Name:                mockito
Version:             2.23.9
Release:             1
Summary:             Tasty mocking framework for unit tests in Java
License:             MIT
URL:                 https://site.mockito.org/
BuildArch:           noarch
Source0:             %{name}-%{version}.tar.xz
Source1:             make-%{name}-sourcetarball.sh
Source2:             mockito-core.pom
Patch0:              use-unbundled-asm.patch
BuildRequires:       maven-local mvn(junit:junit) mvn(net.bytebuddy:byte-buddy)
BuildRequires:       mvn(net.bytebuddy:byte-buddy-agent) mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:       mvn(org.assertj:assertj-core) mvn(org.codehaus.mojo:exec-maven-plugin)
BuildRequires:       mvn(org.hamcrest:hamcrest-core) mvn(org.objenesis:objenesis)
BuildRequires:       mvn(org.ow2.asm:asm)
%description
Mockito is a mocking framework that tastes really good. It lets you write
beautiful tests with clean & simple API. Mockito doesn't give you hangover
because the tests are very readable and they produce clean verification
errors.

%package javadoc
Summary:             Javadocs for %{name}
%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
%patch0
sed -e 's/@VERSION@/%{version}/' %{SOURCE2} > pom.xml
cat > osgi.bnd <<EOF
Automatic-Module-Name: org.mockito
Bundle-SymbolicName: org.mockito
Bundle-Name: Mockito Mock Library for Java.
Import-Package: junit.*;resolution:=optional,org.junit.*;resolution:=optional,org.hamcrest;resolution:=optional,org.mockito*;version="%{version}",*
Private-Package: org.mockito.*
-removeheaders: Bnd-LastModified,Include-Resource,Private-Package
EOF
%mvn_alias org.%{name}:%{name}-core org.%{name}:%{name}-all

%build
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc doc/design-docs/custom-argument-matching.md

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Tue Aug 18 2020 wangyue <wangyue92@huawei.com> - 2.23.9-1
- upgrade the version to 2.23.9

* Thu Apr 23 2020 wutao <wutao61@huawei.com> 1.10.19-19
* delete useless patches

* Thu Apr 2 2020 gulining <gulining1@huawei.com> - 1.10.19-18
- Package init
