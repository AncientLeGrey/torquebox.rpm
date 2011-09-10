require_recipe 'rpmbuild'

jenkins_job 'rpmbuild' do
  plugins [
    'next-build-number',
    'filesystem_scm',
    'batch-task',
    'rake'
  ]
end
