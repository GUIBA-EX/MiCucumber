from pathlib import Path
import subprocess,sys,shutil
p=Path(__file__).resolve().parent/'analysis'
def run(*args): subprocess.run(args,check=True,cwd=p)
run(sys.executable,'validate_targets.py')
run('c++','-O3','-std=c++17','independent_scan.cpp','-o','independent_scan')
run(str(p/'independent_scan'),str(p))
run(sys.executable,'check_independent.py')
run(sys.executable,'evaluate_portfolios.py')
for n in ['target.fasta','background.fasta']: shutil.copyfile(p/n,p/'apodida'/n)
run(str(p/'independent_scan'),str(p/'apodida'))
run(sys.executable,'apodida/summarize.py')
run(sys.executable,'thermal_pairs.py')
run(sys.executable,'thermal_portfolios.py')
run(sys.executable,'apodida/finish.py')
print('Revalidation complete; inspect analysis/*validation.json and results/.')
