bucket="..." # your s3 bucket
template="cloudformation_template.yaml"
output="packaged.yaml"
stack="..." # your cloudformation stack name

sam package \
    --template-file $template \
    --s3-bucket $bucket \
    --output-template-file $output

sam deploy \
    --template-file $output \
    --stack-name $stack \
    --capabilities CAPABILITY_IAM