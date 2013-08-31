
%global base_name  discovery
%global short_name commons-%{base_name}

Name:           apache-%{short_name}
Version:        0.5
Release:        1
Summary:        Apache Commons Discovery
License:        ASL 2.0
Group:          Development/Java
URL:            http://commons.apache.org/%{base_name}
Source0:        http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:	build.xml
Patch0:         %{name}-addosgimanifest.patch
BuildArch:      noarch
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant
BuildRequires:  junit >= 0:3.7
BuildRequires:  commons-logging >= 1.1.1
Requires:       commons-logging >= 1.1.1

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# This should go away with F-17
Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} <= 1:0.4

%description
The Discovery component is about discovering, or finding, implementations for
pluggable interfaces.  Pluggable interfaces are specified with the intent that
multiple implementations are, or will be, available to provide the service
described by the interface.  Discovery provides facilities for finding and
instantiating classes, and for lifecycle management of singleton (factory)
classes.

%package javadoc
Group:          Development/Java
Summary:        API documentation for %{name}
Requires:       jpackage-utils

Obsoletes:      jakarta-%{short_name}-javadoc <= 1:0.4

%description javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
%patch0
cp %{SOURCE1} .

%build
export CLASSPATH=$(build-classpath commons-logging)
ant dist

%install
rm -rf %{buildroot}

# jar
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 dist/%{short_name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

pushd %{buildroot}%{_javadir}
for jar in *-%{version}.jar; do
    ln -sf ${jar} `echo $jar| sed "s|apache-||g"`
    ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
    ln -sf ${jar} `echo $jar| sed "s|apache-\(.*\)-%{version}|\1|g"`
done
popd # come back from javadir

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
%doc LICENSE.txt NOTICE.txt

