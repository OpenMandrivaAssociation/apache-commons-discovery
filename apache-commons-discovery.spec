Name:		apache-commons-discovery
Version:	0.5
Release:	10
Epoch:		2
Summary:	Find implementations of pluggable Java interfaces
Group:		Development/Java
License:	ASL 2.0
URL:		https://commons.apache.org/discovery/
Source0:	https://archive.apache.org/dist/commons/discovery/source/commons-discovery-%{version}-src.tar.gz

BuildArch:	noarch
BuildRequires:	python
BuildRequires:	mvn(org.apache.commons:commons-parent:pom::)
BuildRequires:	mvn(org.apache:apache:pom::)
BuildRequires:	mvn(commons-logging:commons-logging)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name commons-discovery --link %{name}

Provides:	jakarta-commons-discovery = %{epoch}:%{version}-%{release}
Obsoletes:	jakarta-commons-discovery <= 1:0.4
Obsoletes:	%{name}-javadoc < %{epoch}:%{version}-%{release}
Obsoletes:	jakarta-commons-discovery-javadoc <= 1:0.4

%description
Apache Commons Discovery finds and instantiates implementations of
pluggable interfaces. 0.5 is the last upstream release. It needs Java 8
and Commons Logging. Tests are skipped. The automatic module name is
org.apache.commons.discovery.

%prep
%autosetup -n commons-discovery-%{version}-src
# Assembly is bound to package and would attach a second artifact.
# The reporting plugins are not installed.
python - <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path

ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

def local(tag):
    return tag.rsplit("}", 1)[-1]

path = Path("pom.xml")
tree = ET.parse(path)
root = tree.getroot()
removed_asm = 0
for parent in list(root.iter()):
    for child in list(parent):
        if local(child.tag) != "plugin":
            continue
        artifact = ""
        for item in child:
            if local(item.tag) == "artifactId":
                artifact = (item.text or "").strip()
        if artifact == "maven-assembly-plugin":
            parent.remove(child)
            removed_asm += 1
removed_reporting = 0
for child in list(root):
    if local(child.tag) == "reporting":
        root.remove(child)
        removed_reporting += 1
if removed_asm != 1 or removed_reporting != 1:
    raise SystemExit(f"edit failed asm={removed_asm} reporting={removed_reporting}")
tree.write(path, encoding="UTF-8", xml_declaration=True)
text = path.read_text(encoding="utf-8")
if "maven-assembly-plugin" in text or "<reporting>" in text:
    raise SystemExit("pom rewrite failed")
if "<sourceDirectory>src/java</sourceDirectory>" not in text:
    raise SystemExit("source directory missing")
if "commons-logging" not in text:
    raise SystemExit("logging dependency missing")
PY

%build -a
cat > manifest-addition <<'EOF'
Automatic-Module-Name: org.apache.commons.discovery
EOF
jar ufm target/commons-discovery-%{version}.jar manifest-addition
java --module-path target/commons-discovery-%{version}.jar --describe-module org.apache.commons.discovery | grep -q '^org.apache.commons.discovery'

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
