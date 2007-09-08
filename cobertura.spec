%define section         free
%define gcj_support     1
%define build_tests     0

Name:           cobertura
Version:        1.9
Release:        %mkrel 4
Epoch:          0
Summary:        Free Java tool that calculates the percentage of code accessed by tests
Group:          Development/Java
License:        GPL
URL:            http://cobertura.sourceforge.net/
Source0:        http://download.sourceforge.net/cobertura/cobertura-%{version}-src.tar.bz2
Patch0:         %{name}-javadoc.patch
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Requires:       ant >= 0:1.6
Requires:       ant-junit
Requires:       ant-nodeps
Requires:       asm2
Requires:       jpackage-utils >= 0:1.5.32
Requires:       junit
Requires:       log4j
Requires:       oro
Requires:       xerces-j2
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit
BuildRequires:  ant-nodeps
BuildRequires:  asm2
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  jpackage-utils >= 0:1.5.32
BuildRequires:  junit
BuildRequires:  log4j
BuildRequires:  oro
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Cobertura is a free Java tool that calculates the percentage of code 
accessed by tests. It can be used to identify which parts of your 
Java program are lacking test coverage. It is based on jcoverage.

Features:

    * Can be executed from ant or from the command line.
    * Instruments Java bytecode after it has been compiled.
    * Can generate reports in HTML or XML.
    * Shows percent of lines coveraged and branches coveraged for each
      class, package, and for the overall project.
    * Shows the McCabe cyclomatic code complexity of each class, and
      the average cyclomatic code complexity for each package, and for
      the overall product.
    * Can sort HTML results by class name, percent of lines covered,
      percent of branches covered, etc. And can sort in ascending or
      decending order.

NOTE: Due to asm version conflicts, if you use Cobertura as an ant
      task you MUST add manually a classpath element 

        <classpath location="/usr/share/java/asm2/asm2.jar"/>

      to all Cobertura tasks requiring bytecode manipulation.

NOTE: This version does NOT contain the cyclomatic code complexity 
      code because the javancss dependency cannot currently be rebuilt
      from source.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0 -p1
%{__perl} -pi -e 's/1000000/99999/' test/net/sourceforge/cobertura/util/IOUtilTest.java
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}

%build
export CLASSPATH=$(build-classpath ant asm2/asm2 asm2/asm2-tree junit log4j oro xalan-j2 xerces-j2)
export OPT_JAR_LIST="junit ant/ant-junit ant/ant-nodeps"
%{ant} -Dbuild.sysclasspath=last compile \
%if %{build_tests}
test \
%endif
jar javadoc

%install
%{__rm} -rf %{buildroot}

# jar
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a %{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do \
%{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_sysconfdir}/ant.d
%{__cat} > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
ant cobertura junit log4j oro xerces-j2
EOF

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a build/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%{__perl} -pi -e 's/\r$//g;' ChangeLog COPYING COPYRIGHT README
/bin/find examples -type f -exec %{__perl} -pi -e 's/\r$//g;' {} \;

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc ChangeLog COPYING COPYRIGHT README examples
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif
%config(noreplace) %{_sysconfdir}/ant.d/%{name}

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%dir %{_javadocdir}/%{name}
