Name:           mockito
Version:        1.10.19
Release:        18
Summary:        A Java mocking framework
License:        MIT
URL:            http://mockito.org
Source0:        https://github.com/mockito/mockito/archive/v1.10.19.tar.gz
# fix bnd config to resolve build error
Patch0001:      fix-bnd-config.patch
# fix ant script to resolve build error
Patch0002:      fixup-ant-script.patch
# fix build error
Patch0003:      mockito-matcher.patch
# Workaround for NPE in setting NamingPolicy in cglib
Patch0004:      setting-naming-policy.patch
# because we have old objenesis
Patch0005:      fix-incompatible-types.patch
BuildArch:      noarch
BuildRequires:  javapackages-local java-devel ant objenesis cglib
BuildRequires:  junit hamcrest aqute-bnd dos2unix
Requires:       objenesis cglib junit hamcrest

%description
Mockito is a mocking framework that tastes really good. It lets you write
beautiful tests with clean & simple API. Mockito doesn't give you hangover
because the tests are very readable and they produce clean verification
errors.

%package help
Summary:        This package contains help documents
Provides:       mockito-javadoc = %{version}-%{release}
Obsoletes:      mockito-javadoc < %{version}-%{release}

%description help
Files for help with mockito

%prep
%setup -q
rm -rf `find -name *.jar` build.gradle cglib-and-asm doc gradle gradlew gradlew.bat javadoc
dos2unix `find -name *.java`
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%pom_add_dep net.sf.cglib:cglib:3.1 maven/mockito-core.pom
find . -name "*.java" -exec sed -i "s|org\.mockito\.cglib|net\.sf\.cglib|g" {} +
install -d lib/compile
%pom_xpath_remove 'target[@name="javadoc"]/copy' build.xml

%build
build-jar-repository lib/compile objenesis cglib junit hamcrest/core
ant jar javadoc
cd target
bnd wrap --version 1.10.19 --output mockito-core-1.10.19.bar \
 --properties ../conf/mockito-core.bnd mockito-core-1.10.19.jar
mv mockito-core-1.10.19.bar mockito-core-1.10.19.jar
unzip mockito-core-1.10.19.jar META-INF/MANIFEST.MF
sed -i -e '2iRequire-Bundle: org.hamcrest.core' META-INF/MANIFEST.MF
jar umf META-INF/MANIFEST.MF mockito-core-1.10.19.jar
cd ..
sed -i -e "s|@version@|1.10.19|g" maven/mockito-core.pom
%mvn_artifact maven/mockito-core.pom target/mockito-core-1.10.19.jar
%mvn_alias org.mockito:mockito-core org.mockito:mockito-all

%install
%mvn_install -J target/javadoc

%files -f .mfiles
%doc LICENSE

%files help -f .mfiles-javadoc
%doc NOTICE

%changelog
* Thu Apr 2 2020 gulining <gulining1@huawei.com> - 1.10.19-18
- Package init
