%{?_javapackages_macros:%_javapackages_macros}
%global base_name  discovery
%global short_name commons-%{base_name}

Name:           apache-%{short_name}
Version:        0.5
Release:        9.0%{?dist}
Epoch:          2
Summary:        Apache Commons Discovery
License:        ASL 2.0
URL:            http://commons.apache.org/%{base_name}
Source0:        http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch0:         %{name}-addosgimanifest.patch
Patch1:         %{name}-remove-unreliable-test.patch
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  apache-commons-logging >= 1.1.1

Provides:       jakarta-%{short_name} = %{epoch}:%{version}-%{release}
Obsoletes:      jakarta-%{short_name} <= 1:0.4

%description
The Discovery component is about discovering, or finding, implementations for
pluggable interfaces.  Pluggable interfaces are specified with the intent that
multiple implementations are, or will be, available to provide the service
described by the interface.  Discovery provides facilities for finding and
instantiating classes, and for lifecycle management of singleton (factory)
classes.

%package javadoc
Summary:        API documentation for %{name}

Provides:       jakarta-%{short_name}-javadoc = %{epoch}:%{version}-%{release}
Obsoletes:      jakarta-%{short_name}-javadoc <= 1:0.4

%description javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
%patch0
%patch1 -p1

%build
%mvn_file  : %{short_name} %{name}
%mvn_build -X

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Wed Aug 07 2013 Michal Srb <msrb@redhat.com> - 2:0.5-9
- Remove unreliable test (Resolves: #991968)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2:0.5-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 15 2013 Michal Srb <msrb@redhat.com> - 2:0.5-5
- Build with xmvn

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 17 2012 gil cattaneo <puntogil@libero.it> - 2:0.5-3
- add maven pom

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 7 2011 Alexander Kurtakov <akurtako@redhat.com> 2:0.5-1
- Update to 0.5 upstream release.
- Build with maven.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2:0.4-5
- Add license to javadoc subpackage
- Fix jar symlink installation

* Wed May 12 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2:0.4-4
- Add obsoletes to javadoc subpackage
- Add proper symlinks for unversioned jar files

* Fri May  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2:0.4-3
- Add jpackage-utils as dep for -javadoc subpackage

* Fri May  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2:0.4-2
- Fix provides

* Thu May  6 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.4-1
- Rename and cleanup of jakarta-commons-discovery
