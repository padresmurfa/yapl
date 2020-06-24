development:
------------
It is very important that in a project with N yapl files, that you should be able to submit them to N
different AWS lambdas to transpile them. Or just submit the git repo url, version sha, and path, along
with whatever credentials are needed to fetch the files.

to mock a function, it must be declared as a mockable for the function. e.g.

method foo(filename:String) returns blat:boolean mockable(os.path.exists) {
    blat = os.path.exists(filename)
}

-------
Some thoughts...

emitters are specifically testable concepts.
context variables allow setting them and overriding in a nice fashion, using the closure concept
a mock could be interesting such as:

class Foo(bar:String) {
    method durgle() returns blah:String {
    }
    method splat(gurgle:String) returns goo:String {
        function gargleblaster() returns woah:String {
            woah = "WOAH!"
        }
        goo = durgle() + "/" + gurgle + "/" + bar + "/" + gargleblaster()
    }
}

test smurgle for Foo.splat {
    subject = mock Foo(bar = "asdf") {
        method durgle() returns blah:String {
            blah = "meh"
        }
        function splat.gargleblaster() returns woah:String {
            woah = "FARGLESMARGLE!"
        }
    }
    goo = subject.splat("ddd")
    assert(goo == "meh/ddd/asdf/FARGLESMARGLE!", "Goo should be properly durgled by Foo upon splatting, and fargled as well!")
}

// the concept of test dummies...
if you have a running system A, and intend to deploy an update B, then it should be feasible to have the running system A
perform an acceptance test on B.

Say for example that this function exists in the codebase:

function foo(bar:String) returns baz:String {
    if (bar == "A") {
        baz = "aaz"
    } else {
        baz = bar
    }
}

During the lifetime of the process A, it has been invoked as such:

bar="burgle", baz="burgle"
bar="asdf", baz="asdfasdf"
bar="A", baz= "aaz"

then version B could be invoked with the same input values, expecting the same output values.
 
if this does not happen, then A may require that this function in B has full test coverage to accept B into production.  

A may also require that B exhibits no worse runtime performance in a controlled environment. This should typically apply
to entrypoints, such as service endpoints.

```
  @Override
  public boolean validateProjectView(
      @Nullable Project project,
      BlazeContext context,
      ProjectViewSet projectViewSet,
      WorkspaceLanguageSettings workspaceLanguageSettings) {
      
      
    block testable {
        if (!workspaceLanguageSettings.isLanguageActive(LanguageClass.SCALA)) {
          return true;
        }
        if (!PluginUtils.isPluginEnabled(SCALA_PLUGIN_ID)) {
          IssueOutput.error("Scala plugin needed for Scala language support.")
              .navigatable(PluginUtils.installOrEnablePluginNavigable(SCALA_PLUGIN_ID))
              .submit(context);
          return false;
        }
        return true;
      }
    }
}

class UnitTest.validateProjectView.testable {
    class WorkspaceLanguageSettings {
        boolean isLanguageActive(languageClass: LanguageClass)
    }
    class Navigatable {
    }
    class PluginUtils {
        static boolean isPluginEnabled(pluginId: String)
        static Navigatable installOrEnablePluginNavigable(pluginId: String)
    }
    class IssueOutput {
        static IssueOutput error(msg:String)
        IssueOutput navigatable(nav:Navigatable)
        void submit(context:BlazeContext)
    }
  BlazeContext context
  WorkspaceLanguageSettings workspaceLanguageSettings
}

unittest `If the active language is Scala, then the ProjectView is valid` tests validateProjectView.testable {
    context = mock BlazeContext {}
    workspaceLanguageSettings = mock WorkspaceLanguageSettings {
        boolean isLanguageActive(languageClass: LanguageClass) {
            assert(languageClass == LanguageClass.SCALA)
            return true
        }
    }
    returns true    
}

unittest `If the active language is not Scala, but the Scala plugin is enabled, then the ProjectView is valid` tests validateProjectView.testable {
    context = mock BlazeContext {}
    workspaceLanguageSettings = mock WorkspaceLanguageSettings {
        boolean isLanguageActive(languageClass: LanguageClass) {
            assert(languageClass == LanguageClass.SCALA)
            return false
        }
    }
    PluginUtils = mock PluginUtils {
        static boolean isPluginEnabled(pluginId: String) {
            assert(pluginId == SCALA_PLUGIN_ID)
            return true
        }
    }
    returns true    
}

unittest `If the active language is not Scala, and the Scala plugin is not enabled, then the ProjectView is invalid` tests validateProjectView.testable {
    context := mock BlazeContext {}

    workspaceLanguageSettings := mock WorkspaceLanguageSettings {
        // the implementation will ask this to determine whether or not the active language is Scala
        boolean isLanguageActive(languageClass: LanguageClass) {
            assert(languageClass == LanguageClass.SCALA)
            return false
        }
    }

    installOrEnableScalaPluginAction = mock Navigatable {}

    PluginUtils := mock PluginUtils {
        // the implementation will ask this to determine whether or not Scala plugin is enabled
        static boolean isPluginEnabled(pluginId: String) {
            assert(pluginId == SCALA_PLUGIN_ID)
            return false
        }
        // since the Scala plugin is not enabled, the implementation will suggest that the user
        // invoke this to install or enable the plugin
        static Navigatable installOrEnablePluginNavigable(pluginId: String) {
            assert(pluginId == SCALA_PLUGIN_ID)
            return installOrEnableScalaPluginAction
        }
    }

    IssueOutput := mock IssueOutput {
        // the implementation will emit an error message, since the Scala plugin is not enabled 
        static IssueOutput error(msg:String) {
            assert(msg == "Scala plugin needed for Scala language support.")
            return mock new IssueOutput {
                // there will be a navigation option in the error message
                IssueOutput navigatable(nav:Navigatable) {
                    // specifically, the navigation option to install or enable the Scala plugin
                    assert(nav is installOrEnableScalaPluginAction)
                    return this
                }
                // and the issue will have been submitted.
                void submit(ctx:BlazeContext) {
                    assert(ctx is context)
                    // note that the test will fail if mocked code is not reached, so don't worry
                    // about testing whether or not this is invoked 
                }
            }
        }
    }
    returns false
}
```