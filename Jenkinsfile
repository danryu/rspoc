// rspoc - example minimal scripted Pipeline for Lambda deployment 
// Requires:
// - Jenkins Credentials: awscreds, sshcred
// - Jenkins Plugins: Pipeline Steps for AWS, Pipeline Utility

node{
    def bucket = 'rsdemo1'
    def region = 'eu-west-2'
    def function = 'timeFunc'

    stage('Clone'){
        checkout scm
    }

    stage('Test'){
        // scm_repo = scm.getUserRemoteConfigs()[0].getUrl()
        sh "sudo docker pull dxa4481/trufflehog"
        sh "sudo docker run -v jenkins_home:/jenkins_home dxa4481/trufflehog --json --regex file:///jenkins_home/workspace/rspoc/"
    }

    stage('Push to S3'){
        zip zipFile: "${function}.zip", dir: 'lambda_python'

        withAWS(credentials: 'awscreds', region: "${region}") {
            s3Upload([
                bucket: "${bucket}",
                file: "${function}.zip",
            ])
        }   
    }

    stage('Pre Deployment Check') {
        // simply check if the zip file is in the bucket
        withAWS(credentials: 'awscreds', region: "${region}") {
            s3DoesObjectExist bucket: "${bucket}", path: "${function}.zip"
        }
    }

    stage('Deploy Lambda'){
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'awscreds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
            deployLambda([
                artifactLocation: "s3://${bucket}/${function}.zip",
                awsAccessKeyId: "${AWS_ACCESS_KEY_ID}",
                awsRegion: "${region}",
                awsSecretKey: "${AWS_SECRET_ACCESS_KEY}",
                description: 'RiverSafe POC',
                functionName: "${function}",
                handler: "${function}.lambda_handler",
                role: 'arn:aws:iam::132493250445:role/lam_exec_role',
                runtime: 'python3.8',
                updateMode: 'full'
            ])
        }
    }

    stage('Post Deployment Check'){
        // invoke lambda function
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'awscreds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
            step([
                $class: 'LambdaInvokeBuildStep', 
                lambdaInvokeBuildStepVariables: [
                    awsAccessKeyId: "${AWS_ACCESS_KEY_ID}",
                    awsRegion: "${region}",
                    awsSecretKey: "${AWS_SECRET_ACCESS_KEY}",
                    functionName: "${function}",
                    jsonParameters: [[envVarName: 'STATUS_CODE', jsonPath: '$.statusCode']], 
                    synchronous: true
                ]
            ])
        }
    }
}
