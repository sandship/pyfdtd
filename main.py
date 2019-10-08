from fdtdlib import emfield
from fdtdlib import init_param
from fdtdlib import boundary

import sys
import time
import dill

def main():
    # load model and initialize field

    if 'init' in sys.argv:
        param = init_param.InitialzeSpaceParameter()
        efield = emfield.Efield(param)
        hfield = emfield.Hfield(param)
        with open(r"./tmp/pickle/setup_param_pickle.pkl","wb") as fb:
            fb.write(dill.dumps(param))
        with open(r"./tmp/pickle/setup_ef_pickle.pkl", "wb") as fb:
            fb.write(dill.dumps(efield))
        with open(r"./tmp/pickle/setup_hf_pickle.pkl", "wb") as fb:
            fb.write(dill.dumps(hfield))
    elif 'reload' in sys.argv:
        with open(r"./tmp/pickle/setup_param_pickle.pkl", "rb") as fb:
            param = dill.loads(fb.read())
        with open(r"./tmp/pickle/setup_ef_pickle.pkl", "rb") as fb:
            efield = dill.loads(fb.read())
        with open(r"./tmp/pickle/setup_hf_pickle.pkl", "rb") as fb:
            hfield = dill.loads(fb.read())
    else:
        print("!!! You must input subcommand")

    # do computation
    for _ in range(200):
        efield.update_field(hfield)
        hfield.update_field(efield)
        
    # result
    efield.calc_norm()
    efield.calc_phase()


    return None




if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time() - start)