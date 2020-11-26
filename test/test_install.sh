

rm -rf res
mkdir res
cd res

wget https://github.com/cltl/DutchFrameNet/archive/v0.1.zip
unzip v0.1.zip

git clone https://github.com/cltl/FrameNetNLTK
cd FrameNetNLTK
pip install -r requirements.txt
bash install.sh