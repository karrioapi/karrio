# build_files.sh
apt update -y && apt install -y libpango1.0-0 libpangoft2-1.0-0 gcc ghostscript
mkdir -p .karrio
export WORK_DIR=.karrio
pip install -r https://raw.githubusercontent.com/karrioapi/karrio/HEAD/requirements.light.txt
python3.9 -m karrio collectstatic --noinput
