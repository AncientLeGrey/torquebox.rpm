# Become member of ${name} to get the right ruby installation!
# Only for users in the ${name} group
if groups | grep -qF ${name}
then

    umask g+w

    export TORQUEBOX_HOME=${target}
    export TORQUEBOX_VERSION=${version}
    export JBOSS_HOME=$TORQUEBOX_HOME/jboss

    # Use gemset ${name} if user ${name} is member of rvm
    if which rvm > /dev/null
    then
        if groups ${name} | grep -qF rvm
        then
            rvm use ${jrubie}@${name}
            # http://torquebox.org/news/2011/02/25/using-rvm-with-torquebox/
            export JRUBY_HOME=$(rvm info ${jrubie}@${name} homes | grep "ruby:" | cut -d'"' -f2)
        else
            rvm use system
        fi
    fi

    # Use bundled jruby if user ${name} is not in rvm
    if groups ${name} | grep -vqF rvm
    then
        export JRUBY_HOME=$TORQUEBOX_HOME/jruby
    fi

    export PATH=$JRUBY_HOME/bin:$PATH

    # Source a .${name} file for overwriting some settings
    if [ -s "${HOME}/.${name}" ]
    then
        source "${HOME}/.${name}"
    fi

fi
