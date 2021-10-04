region="us-east-1"
stage="dev"

# Returns the status of a stack
Function Get-Status-Of-Stack {
  param($name)
	aws cloudformation describe-stacks --region $region --stack-name $name --query Stacks[].StackStatus --output text 2> Out-Null
}

# Deploy the build to GameLift (Expecting that it was built from Unity already)
Write-Host "Deploying build (Expecting it is prebuilt in HybridGameUnreal\WindowsServer folder)"
$buildversion = Get-Date -UFormat "%y-%m-%d.%H%M%S"
aws gamelift upload-build --operating-system AMAZON_LINUX_2 --build-root ..\HybridGameUnreal\LinuxServer --name "``$stage``-ug-hybrid-gamelift-build" --build-version $buildversion --region $region

# Get the build version for fleet deployment
$query = """Builds[?Version==``$buildversion``].BuildId"""
$buildid = aws gamelift list-builds --query $query --output text --region $region

cdk deploy --profile dev-admin -v -c build_id=$buildid build_version=$buildversion