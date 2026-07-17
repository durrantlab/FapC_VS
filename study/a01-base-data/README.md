
# a01-base-data
This holds initial structural data gotten from previous research. Not used
for any pipeline, just for general visualization

## Data
9NQD.cif: the FapC Model used, [PDB link](https://www.rcsb.org/structure/9NQD)
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
                "https://files.rcsb.org/download/9NQD.cif", 
                "cif"
                ); 
            }
        ); 
    }
); 
</script> 

## Figures
Variety of PyMol scripts that create figures of FapC fibrils / monomers

## Visualization
FapC-fibril-subunit.pse: pymol session where subunit is highlighted
