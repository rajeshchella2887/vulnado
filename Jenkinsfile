pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'chmod +x mvnw'
                sh './mvnw -B clean install'
            }
            post {
              always {
                junit allowEmptyResults: true, testResults: '**/target/surefire-reports/*.xml'
                archiveArtifacts artifacts: 'spring-petclinic-server/target/*.jar', followSymlinks: false
              }
            }
        }
        stage('SonarQube Scan') {
          environment {
            SCANNER_HOME = tool 'SonarQube Scanner'
            PROJECT_NAME = "spring-petclinic-angular"
          }
          steps {
            // sh './mvnw -B sonar:sonar -Dsonar.projectKey=spring-petclinic-angular -Dsonar.host.url=http://10.0.2.38:9000/sonarqube -Dsonar.login=b3a17b16e8766533bc5c077f2af4a6ee7e808ef2'
            withSonarQubeEnv('SonarQube Server') {
                sh '''$SCANNER_HOME/bin/sonar-scanner -Dsonar.java.binaries=spring-petclinic-server/target/classes/ -Dsonar.projectKey=$PROJECT_NAME -Dsonar.sources=.'''
            }
          }
        }
        stage("Push to Nexus") {
          steps {
            script {
              pom = readMavenPom file: "pom.xml";
              filesByGlob = findFiles(glob: "spring-petclinic-server/target/*.jar");
              echo "${filesByGlob[0].name} ${filesByGlob[0].path} ${filesByGlob[0].directory} ${filesByGlob[0].length} ${filesByGlob[0].lastModified}"
              artifactPath = filesByGlob[0].path;
              artifactExists = fileExists artifactPath;
              if (artifactExists) {
                echo "*** File: ${artifactPath}, group: ${pom.groupId}, packaging: jar, version ${pom.version}";
                nexusArtifactUploader(
                artifacts: [[artifactId: pom.artifactId, classifier: '', file: artifactPath, type: 'jar']],
                credentialsId: 'nexus-user-credentials',
                groupId: pom.groupId,
                nexusUrl: '10.0.2.38:8081',
                nexusVersion: 'nexus3',
                protocol: 'http',
                repository: 'ntt-repo',
                version: pom.version);
              }
            }
          }
        }
        stage("Push to DockerHub") {
          steps {
            withCredentials([usernamePassword(credentialsId: 'DockerHub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
              sh 'ansible-playbook -e build_number=${BUILD_NUMBER} -e docker_username=${DOCKER_USERNAME} -e docker_password=${DOCKER_PASSWORD} create-image-playbook.yaml -v'
            }
          }
        }
        stage('Deploy') {
          steps {
            withCredentials([usernamePassword(credentialsId: 'EC2_User', passwordVariable: 'AWS_PASSWORD', usernameVariable: 'AWS_USER')]) {
              sh 'ansible-playbook -e ansible_become_pass=${AWS_PASSWORD} kubernetes/deployment-playbook.yaml -u nttadmin01 -vvv'
            }
          }
        }
    }
}
