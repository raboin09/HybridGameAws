$region="us-east-1"
$stage="dev"

scripts\PostToSlack.bat ":zap: Starting server upload process to ``$region``..."

# Returns the status of a stack
Function Get-Status-Of-Stack {
  param($name)
	aws cloudformation describe-stacks --region $region --stack-name $name --query Stacks[].StackStatus --output text 2> Out-Null
}

$buildversion = Get-Date -UFormat "%y-%m-%d.%H%M%S"
scripts\PostToSlack.bat ":satellite: Creating GameLift Build for ``$buildversion``..."

aws gamelift upload-build --operating-system AMAZON_LINUX_2 --build-root ..\..\..\out\HybridGameUnreal\LinuxServer --name "``$stage``-ug-hybrid-gamelift-build" --build-version $buildversion --region $region

# Get the build version for fleet deployment
$query = """Builds[?Version==``$buildversion``].BuildId"""
$buildid = aws gamelift list-builds --query $query --output text --region $region

Write-Host "Found build id: ``$buildid``"

cdk deploy --profile dev-admin -v -c build_id=$buildid build_version=$buildversion