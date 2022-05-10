### Poseidon notes  

From WHOI VPN or WHCS nextwork:  
`ssh csherwood@poseidon.whoi.edu`

to check on jobs from another ssh 
`squeue -al | grep sherwood`


`mamba install -c conda-forge jupyterlab`

#### Contents of `start_jpy
source activate IOOS
cd /vortexfs1/home/csherwood
echo "ssh -N -L 8888:`hostname`:8888 -L 8787:`hostname`:8787 $USER@poseidon.whoi.edu"
jupyter lab --no-browser --ip=`hostname` --port=8888

