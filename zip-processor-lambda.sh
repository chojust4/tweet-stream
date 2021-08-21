cd handlers

pip install --target ./package requests
pip install --target ./package requests_aws4auth

cd package
zip -r ../processor-deployment-package.zip .

cd ..
zip -g processor-deployment-package.zip processor.py

rm -r package