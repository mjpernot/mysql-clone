pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
        stage('Test') {
            steps {
                dir ('lib') {
                    git branch: "mod/2101", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('mysql_lib') {
                    git branch: "mod/532", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/mysql-lib.git"
                }
                dir ('mysql_lib/lib') {
                    git branch: "mod/294", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                sh """
                virtualenv test_env
                source test_env/bin/activate
                pip2 install mock==2.0.0 --user
                pip2 install mysql-connector-python==8.0.22 --user
                /usr/bin/python ./test/unit/mysql_clone/cfg_chk.py
                /usr/bin/python ./test/unit/mysql_clone/chk_mst_log.py
                /usr/bin/python ./test/unit/mysql_clone/chk_rep.py
                /usr/bin/python ./test/unit/mysql_clone/chk_rep_cfg.py
                /usr/bin/python ./test/unit/mysql_clone/chk_slv.py
                /usr/bin/python ./test/unit/mysql_clone/chk_slv_err.py
                /usr/bin/python ./test/unit/mysql_clone/chk_slv_thr.py
                /usr/bin/python ./test/unit/mysql_clone/connect_chk.py
                /usr/bin/python ./test/unit/mysql_clone/crt_dump_cmd.py
                /usr/bin/python ./test/unit/mysql_clone/dump_load_dbs.py
                /usr/bin/python ./test/unit/mysql_clone/help_message.py
                /usr/bin/python ./test/unit/mysql_clone/main.py
                /usr/bin/python ./test/unit/mysql_clone/run_program.py
                /usr/bin/python ./test/unit/mysql_clone/stop_clr_rep.py
                deactivate
                rm -rf test_env
                """
            }
        }
        stage('SonarQube analysis') {
            steps {
                sh './test/unit/sonarqube_code_coverage.sh'
                sh 'rm -rf lib'
                sh 'rm -rf mysql_lib'
                script {
                    scannerHome = tool 'sonar-scanner';
                }
                withSonarQubeEnv('Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner -Dproject.settings=sonar-project.JACIDM.properties"
                }
            
            }
        }
        stage('Artifactory upload') {
            steps {
                script {
                    server = Artifactory.server('Artifactory')
                    server.credentialsId = 'art-svc-highpoint-dev'
                    uploadSpec = """{
                        "files": [
                            {
                                "pattern": "./*.py",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-clone/"
                            },
                            {
                                "pattern": "./*.txt",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-clone/"
                            },
                            {
                                "pattern": "./*.md",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-clone/"
                            },
                            {
                                "pattern": "*.TEMPLATE",
                                "recursive": true,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-clone/config/"
                            }
                        ]
                    }"""
                    server.upload(uploadSpec)
                }
            }
        }
    }
    post {
        always {
            cleanWs disableDeferredWipeout: true
        }
    }
}
