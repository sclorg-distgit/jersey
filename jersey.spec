%global pkg_name jersey
%{?scl:%scl_package %{pkg_name}}
%global with_grizzly 1
# Use jetty 9.1.1.v20140108.
%bcond_with jetty
%{?java_common_find_provides_and_requires}
Name:          %{?scl_prefix}jersey
Version:       2.18
Release:       3.3%{?dist}
Summary:       JAX-RS (JSR 311) production quality Reference Implementation
# One file in jersey-core/ is under ASL 2.0 license
# https://java.net/jira/browse/JERSEY-2870
License:       (CDDL or GPLv2 with exceptions) and ASL 2.0
URL:           http://jersey.java.net/
Source0:       https://github.com/jersey/jersey/archive/%{version}.tar.gz
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt
# Remove repackaged dependencies: guava, atinject
Patch0:        jersey-2.18-use-system-libraries.patch
# Support fo servlet 3.1 apis
Patch1:        jersey-2.17-mvc-jsp-servlet31.patch
# Update istack plugin reference
Patch2:        jersey-2.17-new-istack-plugin.patch

BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.jaxrs:jackson-jaxrs-base)
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.jaxrs:jackson-jaxrs-json-provider)
BuildRequires: %{?scl_prefix}mvn(com.google.guava:guava)
BuildRequires: %{?scl_prefix_maven}mvn(com.sun.istack:istack-commons-maven-plugin)
BuildRequires: %{?scl_prefix}mvn(javax.annotation:javax.annotation-api)
BuildRequires: %{?scl_prefix_java_common}mvn(javax.inject:javax.inject)
BuildRequires: %{?scl_prefix}mvn(javax.ws.rs:javax.ws.rs-api)
BuildRequires: %{?scl_prefix}mvn(javax.xml.bind:jaxb-api)
BuildRequires: %{?scl_prefix_java_common}mvn(org.apache.httpcomponents:httpclient)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: %{?scl_prefix}mvn(org.glassfish.hk2:hk2-api)
BuildRequires: %{?scl_prefix}mvn(org.glassfish.hk2:hk2-bom:pom:)
BuildRequires: %{?scl_prefix}mvn(org.glassfish.hk2:hk2-locator)
BuildRequires: %{?scl_prefix}mvn(org.glassfish.hk2:osgi-resource-locator)

BuildArch:     noarch

%description
Jersey is the open source JAX-RS (JSR 311)
production quality Reference Implementation
for building RESTful Web services.

%package test-framework
Summary:       Jersey Test Framework

%description test-framework
%{summary}.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{version}
find . -name "*.jar" -print -delete
find . -name "*.class" -print -delete

%patch0 -p1
%patch1 -p1
%patch2 -p1

cp -p %{SOURCE1} .
sed -i 's/\r//' LICENSE-2.0.txt

sed -i '/setConnectionManagerShared/ d' connectors/apache-connector/src/main/java/org/glassfish/jersey/apache/connector/ApacheConnector.java
sed -i '/CONNECTION_MANAGER_SHARED/ d' connectors/apache-connector/src/main/java/org/glassfish/jersey/apache/connector/ApacheConnector.java

%pom_xpath_remove pom:build/pom:extensions

%pom_xpath_remove "pom:plugin[pom:artifactId = 'maven-javadoc-plugin' ]/pom:executions"
%pom_remove_plugin :maven-checkstyle-plugin

# Add OSGi manifest required by docker-client
%pom_add_plugin org.apache.felix:maven-bundle-plugin:2.3.7 connectors/apache-connector '
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>'

# Disable modules we do not need
%pom_disable_module bundles
%pom_disable_module grizzly-connector connectors
%pom_disable_module jetty-connector connectors
%pom_disable_module jaxb media
%pom_disable_module json-jackson1 media
%pom_disable_module json-jettison media
%pom_disable_module json-processing media
%pom_disable_module moxy media
%pom_disable_module multipart media
%pom_disable_module sse media
%pom_disable_module archetypes
%pom_disable_module containers
%pom_disable_module core-server
%pom_disable_module examples
%pom_disable_module bean-validation ext
%pom_disable_module cdi ext
%pom_disable_module metainf-services ext
%pom_disable_module mvc ext
%pom_disable_module mvc-bean-validation ext
%pom_disable_module mvc-freemarker ext
%pom_disable_module mvc-jsp ext
%pom_disable_module mvc-mustache ext
%pom_disable_module proxy-client ext
%pom_disable_module rx ext
%pom_disable_module servlet-portability ext
%pom_disable_module spring3 ext
%pom_disable_module wadl-doclet ext
%pom_disable_module incubator
%pom_disable_module security
%pom_disable_module test-framework
%pom_disable_module tests
# TODO: Ugly way to disable profile-defined module
sed -i '/rx-client-java8/ d' pom.xml

%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin
%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin core-common

%pom_xpath_remove "pom:dependency[pom:scope = 'test' ]" connectors/apache-connector
%pom_xpath_remove "pom:dependency[pom:scope = 'test' ]" ext/entity-filtering

# Avoid building jersey-server
sed -i '/ServerScopeProvider/ d' ext/entity-filtering/src/main/java/org/glassfish/jersey/message/filtering/EntityFilteringFeature.java
sed -i '/SecurityEntityFilteringFeature/ d' ext/entity-filtering/src/main/java/org/glassfish/jersey/message/filtering/EntityFilteringFeature.java

%pom_remove_dep :jersey-server ext/entity-filtering
for f in ServerScopeProvider SecurityEntityFilteringFeature SecurityServerScopeProvider; do
  rm -f ext/entity-filtering/src/main/java/org/glassfish/jersey/message/filtering/$f.java
done

# Conflict with org.glassfish.jersey:project
%mvn_file "org.glassfish.jersey.connectors:project" %{pkg_name}/connectors-project
%mvn_file "org.glassfish.jersey.ext:project" %{pkg_name}/ext-project
%mvn_file "org.glassfish.jersey.media:project" %{pkg_name}/media-project

%{?scl:EOF}

%build

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}

%mvn_build -- -Dmaven.test.skip=true

%{?scl:EOF}

%install

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install

%{?scl:EOF}

%files -f .mfiles
%doc README.md LICENSE.html LICENSE.txt LICENSE-2.0.txt etc/config/copyright.txt
%dir %{_javadir}/jersey
%dir %{_mavenpomdir}/jersey

%files javadoc -f .mfiles-javadoc
%doc LICENSE.html LICENSE.txt LICENSE-2.0.txt etc/config/copyright.txt

%changelog
* Tue Jul 28 2015 Alexander Kurtakov <akurtako@redhat.com> 2.18-3.3
- Drop provides/obsoletes outside of dts namespace.

* Mon Jul 20 2015 Mat Booth <mat.booth@redhat.com> - 2.18-3.2
- Fix unowned directories

* Tue Jul 14 2015 Roland Grunberg <rgrunber@redhat.com> - 2.18-3.1
- SCL-ize.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 gil cattaneo <puntogil@libero.it> 2.18-2
- built with new mimepull rhbz#1189216

* Tue Jun 09 2015 gil cattaneo <puntogil@libero.it> 2.18-1
- update to 2.18
- remove Obsolete duplicate declaration

* Sun Jun  7 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.17-4
- Obsolete jersey-contribs

* Fri May 29 2015 gil cattaneo <puntogil@libero.it> 2.17-3
- remove javax.el:el-api exclusions RHBZ#1223468

* Fri May 29 2015 gil cattaneo <puntogil@libero.it> 2.17-2
- generated apache-connector OSGi manifest

* Fri May 08 2015 gil cattaneo <puntogil@libero.it> 2.17-1
- update to 2.17

* Tue Jan 27 2015 gil cattaneo <puntogil@libero.it> 1.18.3-1
- update to 1.18.3
- introduce license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 05 2014 gil cattaneo <puntogil@libero.it> 1.17.1-10
- fix javax.el apis

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.17.1-9
- Use Requires: java-headless rebuild (#1067528)

* Mon Nov 18 2013 gil cattaneo <puntogil@libero.it> 1.17.1-8
- use objectweb-asm3

* Tue Oct 15 2013 gil cattaneo <puntogil@libero.it> 1.17.1-7
- Do not install source jars

* Tue Oct 15 2013 gil cattaneo <puntogil@libero.it> 1.17.1-6
- fix for rhbz#1019234

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 gil cattaneo <puntogil@libero.it> 1.17.1-4
- switch to XMvn
- minor changes to adapt to current guideline
- fix aId for new istack-commons maven plugin

* Sat Apr 27 2013 gil cattaneo <puntogil@libero.it> 1.17.1-3
- rebuilt with grizzly support

* Thu Mar 28 2013 gil cattaneo <puntogil@libero.it> 1.17.1-2
- fixed license field
- installed ASL license txt file

* Mon Mar 18 2013 gil cattaneo <puntogil@libero.it> 1.17.1-1
- update to 1.17.1

* Tue Jan 22 2013 gil cattaneo <puntogil@libero.it> 1.17-1
- update to 1.17

* Fri Jan 11 2013 gil cattaneo <puntogil@libero.it> 1.16-1
- update to 1.16

* Mon Nov 19 2012 gil cattaneo <puntogil@libero.it> 1.15-1
- update to 1.15

* Tue Sep 18 2012 gil cattaneo <puntogil@libero.it> 1.14-1
- update to 1.14

* Sat Jul 21 2012 gil cattaneo <puntogil@libero.it> 1.13-1
- update to 1.13

* Fri May 25 2012 gil cattaneo <puntogil@libero.it> 1.12-1
- initial rpm
