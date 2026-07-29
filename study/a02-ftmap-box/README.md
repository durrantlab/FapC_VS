
# a02-ftmap-box
Goal: determine docking boxes using FTMap.
*This was all run previously, therefore just holds output from that*

## Data
9nqd.fftmap.output.pdb: PDB output from FTMap with FTMap molecular probes
<script>
document.addEventListener(
    'DOMContentLoaded',
    (event) => {
        const viewer = molstar.Viewer.create(
            'Top-Structure-view',
            {
                layoutIsExpanded: false,
                layoutShowControls: false,
                layoutShowRemoteState: false,
                layoutShowSequence: true,
                layoutShowLog: false,
                layoutShowLeftPanel: false,
                viewportShowExpand: true,
                viewportShowSelectionMode: true,
                viewportShowAnimation: false,
                pdbProvider: 'rcsb',
            }
        ).then(viewer => {
            viewer.loadStructureFromUrl(
                "data/9nqd.fftmap.output.pdb",
                "pdb"
            );
        });
    }
);
</script>
9nqd.fftmap.cleared.pdb: PDB output from FTMap, docked molecules removed. Same as input
box/region_#.txt: each box output from FTMap. Has format required for GNINA

## Figures
boxes_highlighted.pml: protein with highlighted boxes.
no_boxes.pml: protein without boxes

## Visualization
[boxes_highlighted.pml](/visualization/boxes_highlighted.pml): sets up seesion with boxes present
    All .pml scripts point to 9nqd.fftmap.cleared.pdb in data

