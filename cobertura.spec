# Prevent brp-java-repack-jars from being run
%global __jar_repack %{nil}

Name:           cobertura
Version:        1.9.3
Release:        3
Summary:        Java tool that calculates the percentage of code accessed by tests

Group:          Development/Java
License:        ASL 1.1 and GPLv2+
URL:            http://cobertura.sourceforge.net/

Source0:        http://prdownloads.sourceforge.net/cobertura/cobertura-1.9.3-src.tar.gz
Source1:        %{name}-%{version}.pom
Source2:        %{name}-runtime-%{version}.pom

BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  ant-trax
BuildRequires:  antlr
BuildRequires:  dos2unix
BuildRequires:  groovy
BuildRequires:  jpackage-utils
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  jakarta-oro
BuildRequires:  jaxen
BuildRequires:  jdom
BuildRequires:  junit4
BuildRequires:  log4j
BuildRequires:  objectweb-asm
BuildRequires:  tomcat6-servlet-2.5-api
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  jakarta-commons-cli

Requires:       ant
Requires:       jpackage-utils
Requires:       java >= 0:1.6.0
Requires:       jakarta-oro
Requires:       junit4
Requires:       log4j
Requires:       objectweb-asm >= 0:3.0

Requires(post): jpackage-utils
Requires(postun): jpackage-utils

BuildArch:      noarch

%description
Cobertura is a free Java tool that calculates the percentage of code
accessed by tests. It can be used to identify which parts of your
Java program are lacking test coverage.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description    javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
find . -type f -name '*.jar' -delete

sed -i 's/\r//' ChangeLog COPYING COPYRIGHT README

# fix asm depdency to correct groupId
sed -i 's/org.objectweb.asm/asm/g' %{SOURCE1} %{SOURCE2}

%build
pushd lib
  %__ln_s $(build-classpath jaxen) .
  %__ln_s $(build-classpath jdom) .
  %__ln_s $(build-classpath junit4) .
  %__ln_s $(build-classpath log4j) .
  %__ln_s $(build-classpath objectweb-asm/asm-all) .
  %__ln_s $(build-classpath oro) .
  %__ln_s $(build-classpath xalan-j2) .
  %__ln_s $(build-classpath tomcat6-servlet-2.5-api) servlet-api.jar
  %__ln_s $(build-classpath apache-commons-cli) commons-cli.jar
  pushd xerces
    %__ln_s $(build-classpath xalan-j2) .
    %__ln_s $(build-classpath xml-commons-jaxp-1.3-apis) .
  popd
popd

pushd antLibrary/common
  %__ln_s $(build-classpath groovy) .
popd

export CLASSPATH=$(build-classpath objectweb-asm/asm-all commons-cli antlr junit4)
%ant -Djetty.dir=. -Dlib.dir=. compile test jar javadoc

%install
# jar
%__mkdir_p %{buildroot}%{_javadir}
%__cp -a %{name}.jar %{buildroot}%{_javadir}/%{name}.jar

%add_to_maven_depmap cobertura cobertura %{version} JPP %{name}
%add_to_maven_depmap cobertura cobertura-runtime %{version} JPP %{name}
%add_to_maven_depmap net.sourceforge.cobertura cobertura %{version} JPP %{name}
%add_to_maven_depmap net.sourceforge.cobertura cobertura-runtime %{version} JPP %{name}

# pom
%__mkdir_p %{buildroot}%{_mavenpomdir}
%__cp -a %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%__cp -a %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP-%{name}-runtime.pom

%__mkdir_p  %{buildroot}%{_sysconfdir}/ant.d
%__cat > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
ant cobertura junit4 log4j oro xerces-j2
EOF

# javadoc
%__mkdir_p %{buildroot}%{_javadocdir}/%{name}
%__cp -a build/api/* %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING COPYRIGHT README
%{_javadir}/*.jar
%config(noreplace) %{_sysconfdir}/ant.d/%{name}
%{_mavenpomdir}/JPP-%{name}*.pom
%config(noreplace) %{_mavendepmapfragdir}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}

