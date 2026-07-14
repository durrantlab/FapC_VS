import argparse
import csv
import json
import sys
import time
from pathlib import Path

import requests

SERVER = "https://pharmit.csb.pitt.edu/fcgi-bin/pharmitserv.fcgi"

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()


class PharmitError(RuntimeError):
    pass


def run(
    query_path: Path,
    out_path: Path,
    interval: float,
    timeout: float,
    csv_path: Path | None = None,
    max_mol: int = 2000,
) -> bool:
    """Overall, takes in pharmacophore list, calls the server, then returns the SDF


    Args:
        query_path: location of pharmacophore list
        out_path: location where SDF will be placed
                        make sure file does not already exist before running
        interval: how often to check server when waiing for response
        timeout: how long before saying server is timed out
        csv_path: location where the csv of molecule ranking is placed
                        make sure file does not already exist before running
        max_mol: max number of molecules to return

    Returns:
        Boolean if the search successfully found molecules or not
    """
    if csv_path is None:
        csv_path = out_path.with_suffix(".csv")
    if csv_path.is_file() or out_path.is_file():
        print(" WARNING: PHARMIT OUTPUT FILE(S) ALREADY EXIST. OVERWRITING")

    # read in the pharmacophore file
    query = json.loads(query_path.read_text())
    n_enabled = sum(1 for p in query.get("points", []) if p.get("enabled"))
    print(f" loaded query: {len(query.get('points', []))} points ({n_enabled} enabled)")

    # add filters to search
    apply_search_filters(query, max_mol)

    # access the pharmit server
    success = False
    with requests.Session() as session:
        # setup the pharmacophores, molecular library, and search parameters
        started = start_query(session, query)
        qid = started["qid"]  # qid: query ID, ID of this session
        try:
            # run pharmacophore search on server and wait for it to complete
            total = poll(session, qid, interval=interval, timeout=timeout)
            if total > 0:
                save_results(session, qid, out_path)
                save_rmsd_csv(session, qid, csv_path, total)
                success = True
            else:
                print(" no hits; skipping saveres")
        finally:
            cancel(session, qid)
    return success


def apply_search_filters(query: dict, max_mol: int) -> dict:
    """Add extra search filters / parameters to query dictionary

    Args:
        query: the pharmacophore query JSON (modified in place)

    Returns:
        dict: the same query dict, with the filter keys set
    """
    # random settings
    temp = {
        "ShapeModeSelect": "filter",
        "inselect": "none",
        "intolerance": 1,
        "inshapestyle": "inshapestyle-solid",
        "exselect": "none",
        "extolerance": 1,
        "exshapestyle": "exshapestyle-solid",
        "minMolWeight": "",
        "minrotbonds": "",
        "maxrotbonds": "",
        "minlogp": "",
        "maxlogp": "",
        "minpsa": "",
        "maxpsa": "",
        "minaromatics": "",
        "maxaromatics": "",
        "minhba": "",
        "maxhba": "",
        "minhbd": "",
        "maxhbd": "",
    }
    query.update(temp)

    # cap the total number of returned hits
    query["max-hits"] = max_mol
    # cap max weight
    query["maxMolWeight"] = 750
    # set to molport dataset
    query["subset"] = "molport"
    # only return top orientation for each molecule
    query["max-orient"] = 1
    query["reduceConfs"] = 1

    print(
        f" applied filters: max-hits={query['max-hits']}, max molecular weight={query['maxMolWeight']} Da, dataset={query['subset']}"
    )
    return query


def start_query(
    session: requests.Session, query: dict, old_qid: int | None = None
) -> dict:
    """Submits a 'startquery' to the server, which will setup session with the
    pharmacophores and the molecule library

    Args:
        session (Session): the website querying session
        query: the pharmacophore JSON
        old_qid (int, optional):

    Returns:
        dict: data returned from startquery submission
    """
    # setups server query and sends it
    payload = {"cmd": "startquery", "json": json.dumps(query)}
    """data sent to the server"""
    if old_qid is not None:
        payload["oldqid"] = old_qid
    resp = session.post(SERVER, data=payload, timeout=60)

    # waits for response and stores it in data
    resp.raise_for_status()
    data = resp.json()
    if not data.get("status"):
        raise PharmitError(f"startquery rejected: {data.get('msg', 'unknown error')}")
    print(
        f" query accepted qid={data['qid']} searching {data.get('numMols', '?')} mols / {data.get('numConfs', '?')} confs"
    )
    return data


def poll(
    session: requests.Session, qid: int, interval: float = 1.0, timeout: float = 600.0
) -> int:
    """Will run the pharmacophore search on server, wait for it to complete (sending
    updates as the server gives them), then returns total found.

    Args:
        session (Session): the website querying session
        qid: server session id. Comes from when session initially setup
        interval: how long to wait between server pings
        timeout: how long before deciding server timed out

    Returns:
        int: how many molecules found
    """

    params = {
        "cmd": "getdata",
        "qid": qid,
        "draw": 1,
        "start": 0,
        "length": 1,
        # default sort matches the pharmacophore table (RMSD ascending)
        "order[0][column]": 1,
        "order[0][dir]": "asc",
    }
    """The data sent to the server. Tells it to do pharm search"""

    deadline = time.monotonic() + timeout
    while True:
        # submits pharm search to server
        resp = session.post(SERVER, data=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()  # a response does not mean search is done

        if data.get("status") == 0:
            raise PharmitError(f"search error: {data.get('msg', 'unknown error')}")

        # once complete, return search is complete
        total = data.get("recordsTotal", 0)
        if data.get("finished"):
            print(f" search finished: {total} hits")
            return total

        # print info in last server response
        print(f" still searching... {total} hits so far")
        if time.monotonic() > deadline:
            raise PharmitError(f"poll timed out after {timeout}s (qid={qid})")
        time.sleep(interval)


def save_results(session: requests.Session, qid: int, out_path: Path) -> Path:
    """Download the full hit set as SDF via saveres.

    Args:
        session (Session): the website querying session
        qid: server session id. Comes from when session initially setup
        out_path: dir where SDF file will be placed

    Returns:
        Path: specific SDF file path
    """
    # query for SDF file
    resp = session.post(SERVER, data={"cmd": "saveres", "qid": qid}, timeout=300)
    resp.raise_for_status()
    # write out the SDF file
    out_path.write_bytes(resp.content)
    print(f" wrote {len(resp.content)} bytes -> {out_path}")
    return out_path


def fetch_all_rows(
    session: requests.Session, qid: int, total: int, page: int = 1000
) -> list:
    """Pull every result row from the finished search via paged 'getdata' calls.

    Args:
        session (Session): the website querying session
        qid: server session id
        total: number of hits to retrieve (from poll())
        page: how many rows to request per call

    Returns:
        list: all result rows, each a list like [name, rmsd, mass, ...]
    """
    rows: list = []
    start = 0
    draw = 2  # poll() used draw=1; keep draw values distinct per request
    while start < total:
        length = min(page, total - start)
        params = {
            "cmd": "getdata",
            "qid": qid,
            "draw": draw,
            "start": start,
            "length": length,
            # keep the same RMSD-ascending ordering as poll()
            "order[0][column]": 1,
            "order[0][dir]": "asc",
        }
        resp = session.post(SERVER, data=params, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        chunk = data.get("data", [])
        if not chunk:
            # nothing more came back; stop rather than loop forever
            break
        rows.extend(chunk)
        start += len(chunk)
        draw += 1

    print(f" fetched {len(rows)} of {total} result rows")
    return rows


def save_rmsd_csv(
    session: requests.Session, qid: int, csv_path: Path, total: int
) -> Path:
    """Write a CSV of molecule name and RMSD for every hit in the search.

    Format: first row is name, rmsd always. Each row is each different
    molecule's full name and best RMSD. Invalid rows should be fully deleted

    Args:
        session (Session): the website querying session
        qid: server session id
        csv_path: where the CSV will be written
        total: number of hits (from poll())

    Returns:
        Path: the CSV file path
    """
    rows = fetch_all_rows(session, qid, total)

    with open(csv_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["name", "rmsd"])
        for row in rows:
            try:
                if len(row) > 1 and isinstance(row[1], float):
                    name = row[0]
                    rmsd = row[1]
                    writer.writerow([name, rmsd])
            except Exception:
                pass

    print(f" wrote {len(rows)} rows -> {csv_path}")
    return csv_path


def cancel(session: requests.Session, qid: int) -> None:
    """Free a running/finished query server-side."""
    try:
        session.post(SERVER, data={"cmd": "cancelquery", "oldqid": qid}, timeout=30)
        print(f" session canceled {qid}")
    except requests.RequestException:
        pass  # best effort


if __name__ == "__main__":
    query_path: Path = (
        DIR_STUDY
        / "031-validate-pharm-top-div"
        / "data"
        / "region_1"
        / "reg_1_mol1_base_input.json"
    ).resolve()
    out_path: Path = (
        DIR_SCRIPT / ".." / "data" / "search_output" / "region_1" / "mol1" / "op.sdf"
    ).resolve()
    interval: float = 16.0
    timeout: float = 600.0
    run(query_path, out_path, interval, timeout, None)
