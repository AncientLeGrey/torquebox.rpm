jenkins_job 'build' do
  tool 'maven'
  plugins [
    'github',
    'git'
  ]
end
