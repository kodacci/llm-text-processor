def PROJECT_VERSION
def DEPLOY_GIT_SCOPE
def APP_IMAGE_TAG

static def genImageTag(name, scope, version, buildNumber) {
    return 'pro.ra-tech/giga-ai-agent/' +
            scope + '/' + name + ':' +
            version + '-' + buildNumber
}

def buildImage(name, dockerFilePath, scope, version, buildNumber) {
    def tag = genImageTag(name, scope, version, buildNumber)

    docker.withServer(DOCKER_HOST, 'jenkins-client-cert') {
        echo "Building image with tag '$tag'"
        def image = docker.build(tag, '-f ' + dockerFilePath + ' .')

        docker.withRegistry(SNAPSHOTS_DOCKER_REGISTRY_HOST, 'vault-nexus-deployer') {
            image.push()
            image.push('latest')
        }
    }

    return tag
}

pipeline {
    agent any

    options {
        ansiColor('xterm')
    }

    stages {
        stage('Determine Version') {
            steps {
                script {
                    withPythonEnv('Python-3') {
                        println 'Getting python version'
                        sh 'python --version'

                        sh 'pip install -U hatch'
                        sh 'hatch --version'

                        PROJECT_VERSION = sh(script: 'hatch version', encoding: 'UTF-8', returnStdout: true).trim()
                        DEPLOY_GIT_SCOPE =
                                sh(encoding: 'UTF-8', returnStdout: true, script: 'git name-rev --name-only HEAD')
                                        .trim()
                                        .tokenize('/')
                                        .last()
                                        .toLowerCase()
                        echo "Project version: '${PROJECT_VERSION}'"
                        echo "Git branch scope: '${DEPLOY_GIT_SCOPE}'"
                    }
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    println("Building project version: $PROJECT_VERSION")

                    def logFileName = env.BUILD_TAG + '-build.log'
                    try {
                        withPythonEnv('Python-3') {
                            sh 'pip install -U hatch'
                            sh 'hatch env create prod'
                            sh "hatch -v build -t wheel"
                        }
                    } finally {
//                        archiveArtifacts(logFileName)
//                        sh "rm \"$logFileName\""
                    }
                }

                println('Build finished')
            }
        }

        stage('Deploy to Nexus Snapshots') {
            when {
                not {
                    branch 'release/*'
                }
            }

            steps {
                script {
                    println('Deploying to Nexus snapshots')

                    withPythonEnv('Python-3') {
                        sh 'pip install -U twine'

                        withCredentials([usernamePassword(
                                credentialsId: 'vault-nexus-deployer',
                                usernameVariable: 'TWINE_USERNAME',
                                passwordVariable: 'TWINE_PASSWORD'
                        )]) {
                            sh "twine upload --repository-url $NEXUS_PYPI_SNAPSHOTS dist/*"
                        }
                    }

                    println('Deploying to Nexus finished')
                }
            }
        }

        stage('Build docker image') {
            steps {
                script {
                    APP_IMAGE_TAG = buildImage(
                            'llm-text-processor',
                            'distrib/docker/Dockerfile',
                            DEPLOY_GIT_SCOPE,
                            PROJECT_VERSION,
                            currentBuild.number
                    )
                }
            }
        }
    }
}
