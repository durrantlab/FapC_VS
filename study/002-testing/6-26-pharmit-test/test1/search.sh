["pixi","run","-e","pharmit","pharmit","dbsearch","-max-weight","750",
                      "-extra-info","-sort-rmsd","-in",str(pharm_file),"-out",
		                            str(pharmit_output_dir),"-max-hits",str(max_mol)]
					        all_db_paths: list[Path] = [item for item in pharm_db_dir.iterdir() if item.is_dir()]
						    for db_path in all_db_paths:
							            cmd.append("-dbdir")
								            cmd.append(str(db_path))
