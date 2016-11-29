%{?scl:%scl_package jersey}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

# Use jetty 9.1.1.v20140108.
%bcond_with jetty
Name:          %{?scl_prefix}jersey
Version:       2.22.2
Release:       1.%{baserelease}%{?dist}
Summary:       JAX-RS (JSR 311) production quality Reference Implementation
# One file in jersey-core/ is under ASL 2.0 license
License:       (CDDL or GPLv2 with exceptions) and ASL 2.0
URL:           http://jersey.java.net/
Source0:       https://github.com/jersey/jersey/archive/%{version}.tar.gz
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

# Support fo servlet 3.1 apis
Patch1:        jersey-2.17-mvc-jsp-servlet31.patch
# Support for simple 6.0.1
Patch2:        jersey-2.22.2-simple.patch

BuildRequires: %{?scl_prefix_maven}maven-local
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.jaxrs:jackson-jaxrs-base)
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.jaxrs:jackson-jaxrs-json-provider)
BuildRequires: %{?scl_prefix}mvn(com.google.guava:guava)
BuildRequires: %{?scl_prefix_maven}mvn(com.sun.istack:istack-commons-maven-plugin)
BuildRequires: %{?scl_prefix_java_common}mvn(commons-io:commons-io)
BuildRequires: %{?scl_prefix_java_common}mvn(commons-logging:commons-logging)
BuildRequires: %{?scl_prefix}mvn(javax.annotation:javax.annotation-api)
BuildRequires: %{?scl_prefix_java_common}mvn(javax.el:javax.el-api)
BuildRequires: %{?scl_prefix_java_common}mvn(javax.inject:javax.inject)
BuildRequires: %{?scl_prefix}mvn(javax.servlet:javax.servlet-api)
BuildRequires: %{?scl_prefix_java_common}mvn(javax.servlet.jsp:javax.servlet.jsp-api)
BuildRequires: %{?scl_prefix}mvn(javax.ws.rs:javax.ws.rs-api)
BuildRequires: %{?scl_prefix}mvn(javax.xml.bind:jaxb-api)
BuildRequires: %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires: %{?scl_prefix_maven}mvn(net.java:jvnet-parent:pom:)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: %{?scl_prefix_java_common}mvn(org.apache.httpcomponents:httpclient)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires: %{?scl_prefix_maven}mvn(org.codehaus.jettison:jettison)
BuildRequires: %{?scl_prefix_maven}mvn(org.codehaus.mojo:build-helper-maven-plugin)
%if %{with jetty}
BuildRequires: %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-client)
BuildRequires: %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-continuation)
BuildRequires: %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-server)
BuildRequires: %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-util)
BuildRequires: %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-webapp)
%endif
BuildRequires: %{?scl_prefix}mvn(org.glassfish.hk2:hk2-api)
BuildRequires: %{?scl_prefix}mvn(org.glassfish.hk2:hk2-bom:pom:)
BuildRequires: %{?scl_prefix}mvn(org.glassfish.hk2:hk2-locator)
BuildRequires: %{?scl_prefix}mvn(org.glassfish.hk2:osgi-resource-locator)
BuildRequires: %{?scl_prefix}mvn(org.glassfish.web:javax.el)
BuildRequires: %{?scl_prefix_java_common}mvn(org.hamcrest:hamcrest-library)
BuildRequires: %{?scl_prefix_maven}mvn(org.osgi:org.osgi.core)
BuildRequires: %{?scl_prefix_java_common}mvn(org.ow2.asm:asm-all:5)
BuildRequires: %{?scl_prefix_maven}mvn(org.testng:testng)
BuildRequires: %{?scl_prefix_java_common}mvn(xerces:xercesImpl)

Obsoletes:     %{?scl_prefix}maven-wadl-plugin
Provides:      %{name}-contribs
Obsoletes:     %{name}-contribs < 2.17-1

BuildArch:     noarch

%description
Jersey is the open source JAX-RS (JSR 311)
production quality Reference Implementation
for building RESTful Web services.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n %{pkg_name}-%{version}
find . -name "*.jar" -print -delete
find . -name "*.class" -print -delete

%patch1 -p1
%patch2 -p1

# Remove repackaged dependencies: guava, atinject
sed -i '/jersey.repackaged/d' \
 ext/cdi/jersey-cdi1x/src/main/java/org/glassfish/jersey/ext/cdi1x/internal/CdiComponentProvider.java
find ./ -name "*.java" -exec sed -i "s|jersey.repackaged.||" {} +
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 containers/grizzly2-http
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 containers/jersey-servlet-core
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 containers/jetty-http
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 containers/simple-http
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 core-client
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 core-common
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 core-server
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 ext/bean-validation
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 ext/mvc-jsp
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 media/jaxb
%pom_change_dep org.glassfish.hk2.external:javax.inject javax.inject:javax.inject:1 media/sse
%pom_change_dep org.glassfish.jersey.bundles.repackaged:jersey-guava com.google.guava:guava:'${guava.version}' bom
%pom_change_dep org.glassfish.jersey.bundles.repackaged:jersey-guava com.google.guava:guava:'${guava.version}' core-common
%pom_change_dep -r org.glassfish.hk2.external:aopalliance-repackaged aopalliance:aopalliance:1.0

# Force servlet 3.1 apis
%pom_change_dep -r :servlet-api :javax.servlet-api
%pom_xpath_set "pom:properties/pom:servlet2.version" 3.1.0
%pom_xpath_set "pom:properties/pom:servlet3.version" 3.1.0
%pom_remove_dep -r org.mortbay.jetty:servlet-api-2.5
%pom_remove_dep -r org.jmockit:jmockit

%pom_xpath_set -r "pom:plugin[pom:groupId = 'com.sun.istack' ]/pom:artifactId" istack-commons-maven-plugin

cp -p %{SOURCE1} .
sed -i 's/\r//' LICENSE-2.0.txt

%pom_xpath_remove pom:build/pom:extensions

%pom_remove_plugin :buildnumber-maven-plugin
%pom_remove_plugin :buildnumber-maven-plugin core-common
%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin -r :maven-source-plugin
%pom_remove_plugin :maven-jflex-plugin media/moxy
%pom_remove_plugin :maven-jflex-plugin media/jaxb
%pom_remove_plugin :maven-shade-plugin core-server

%pom_xpath_remove "pom:plugin[pom:artifactId = 'maven-javadoc-plugin' ]/pom:executions"
%pom_remove_plugin :maven-checkstyle-plugin

%pom_disable_module archetypes
%pom_disable_module bundles
%pom_remove_dep org.glassfish.jersey.bundles: bom
%pom_remove_dep org.glassfish.jersey.bundles.repackaged: bom
%pom_disable_module jersey-guava bundles/repackaged
%pom_disable_module examples
%pom_disable_module examples/feed-combiner-java8-webapp
%pom_disable_module examples/java8-webapp
%pom_disable_module examples/rx-client-java8-webapp
%pom_disable_module gae-integration incubator
%pom_disable_module html-json incubator
# org.codehaus.groovy:groovy-eclipse-compiler:2.9.2-01
%pom_disable_module container-runner-maven-plugin test-framework/maven

# Use jersey-jsr166e bundle of Doug Lea's JCP JSR-166 APIS
%pom_disable_module rx-client-jsr166e ext/rx
%pom_remove_dep :jersey-rx-client-jsr166e bom
# org.glassfish.grizzly:grizzly-http-client:1.8
%pom_disable_module grizzly-connector connectors
%pom_remove_dep :jersey-grizzly-connector bom
# Use com.sun.jersey:jersey-servlet:1.17
%pom_disable_module servlet-portability ext
%pom_remove_dep :jersey-servlet-portability bom
%pom_disable_module tests
%pom_disable_module glassfish containers
%pom_remove_dep :jersey-gf-ejb bom

%if %{without jetty}
# Add support for jetty 9.3.0.M2
%pom_disable_module jetty-connector connectors
%pom_disable_module jetty-http containers
%pom_disable_module jetty-servlet containers
%pom_disable_module jetty test-framework/providers
%pom_remove_dep :jersey-container-jetty-http bom
%pom_remove_dep :jersey-container-jetty-servlet bom
%pom_remove_dep :jersey-jetty-connector bom
%pom_remove_dep :jersey-jetty-connector media/multipart
%pom_remove_dep :jersey-test-framework-provider-jetty bom
%pom_remove_dep :jersey-test-framework-provider-jetty test-framework/providers/bundle
%endif

# eclipselink:2.6.0
%pom_disable_module moxy media
%pom_remove_dep :jersey-media-moxy bom

# Fix asm aId (asm-debug-all)
%pom_xpath_set "pom:dependency[pom:groupId = 'org.ow2.asm']/pom:artifactId" asm-all
%pom_xpath_set "pom:dependency[pom:groupId = 'org.ow2.asm']/pom:artifactId" asm-all core-server
%pom_xpath_set "pom:dependency[pom:groupId = 'org.ow2.asm']/pom:artifactId" asm-all test-framework

# Prepare offline setting for generate java source code
cat > core-server/etc/bindings.cat << EOFCAT
PUBLIC "-//W3C//DTD XMLSchema 200102//EN" "XMLSchema.dtd"
PUBLIC "XMLSchema" "XMLSchema.dtd"
SYSTEM "XMLSchema.dtd" "XMLSchema.dtd"

PUBLIC "datatypes" "datatypes.dtd"
SYSTEM "datatypes.dtd" "datatypes.dtd"

SYSTEM "xml.xsd" "xml.xsd"
EOFCAT
rm -r core-server/etc/catalog.xml core-server/src/main/java/com/sun/research/ws/wadl
sed -i 's|schemaLocation="http://www.w3.org/2001/xml.xsd"|schemaLocation="./xml.xsd"|' core-server/etc/wadl.xsd

# Update plugin references
%pom_remove_plugin com.sun.tools.xjc.maven2: core-server
%pom_add_plugin "org.jvnet.jaxb2.maven2:maven-jaxb22-plugin:0.12.3" core-server '
<executions>
  <execution>
    <id>bindings</id>
    <phase>generate-sources</phase>
    <goals>
      <goal>generate</goal>
    </goals>
    <configuration>
      <generatePackage>com.sun.research.ws.wadl</generatePackage>
      <catalog>${basedir}/etc/bindings.cat</catalog>
      <schemaDirectory>${basedir}/etc</schemaDirectory>
      <bindingDirectory>${basedir}</bindingDirectory>
      <bindingIncludes>
        <bindingInclude>wadl.xsd</bindingInclude>
      </bindingIncludes>
      <forceRegenerate>false</forceRegenerate>
      <episode>true</episode>
      <specVersion>2.1</specVersion>
      <extension>true</extension>
      <strict>false</strict>
    </configuration>
  </execution>
</executions>'

%pom_xpath_remove "pom:surefire.security.argline" core-common
%pom_xpath_remove "pom:surefire.security.argline" core-server

%pom_remove_dep :javaee-api ext/cdi/jersey-cdi1x-transaction
# package javax.enterprise.context javax.enterprise.event javax.enterprise.inject.spi does not exist
%pom_add_dep javax.enterprise:cdi-api:'${cdi.api.version}':provided ext/cdi/jersey-cdi1x-transaction
# package javax.interceptor does not exist
%pom_add_dep org.jboss.spec.javax.interceptor:jboss-interceptors-api_1.2_spec:1.0.0.Alpha3:provided ext/cdi/jersey-cdi1x-transaction
%pom_add_dep org.jboss.spec.javax.interceptor:jboss-interceptors-api_1.2_spec:1.0.0.Alpha3:provided ext/cdi/jersey-cdi1x-validation
# cannot find symbol javax.transaction.Transactional javax.transaction.TransactionalException
%pom_add_dep org.jboss.spec.javax.transaction:jboss-transaction-api_1.2_spec:1.0.0.Alpha3:provided ext/cdi/jersey-cdi1x-transaction

%pom_xpath_remove "pom:dependencies/pom:dependency[pom:artifactId = 'tools']/pom:scope" ext/wadl-doclet
%pom_xpath_remove "pom:dependencies/pom:dependency[pom:artifactId = 'tools']/pom:systemPath" ext/wadl-doclet

# ClassNotFoundException: javax.json.JsonStructure
%pom_add_dep javax.json:javax.json-api:1.0 media/json-processing

# Change scope form test to ..., cause: package com.google.common.util.concurrent does not exist
%pom_xpath_set "pom:dependency[pom:artifactId = 'guava']/pom:scope" provided connectors/apache-connector
%pom_xpath_set "pom:dependency[pom:artifactId = 'guava']/pom:scope" provided containers/jdk-http

# NoClassDefFoundError: org/objectweb/asm/ClassVisitor
%pom_add_dep org.ow2.asm:asm-all:5.0.3:test containers/jdk-http
%pom_add_dep org.ow2.asm:asm-all:5.0.3:test containers/simple-http
%pom_add_dep org.ow2.asm:asm-all:5.0.3:test media/json-processing

# Jersey core server unit tests should run with active security manager
rm -r core-common/src/test/java/org/glassfish/jersey/SecurityManagerConfiguredTest.java
rm -r core-server/src/test/java/org/glassfish/jersey/server/SecurityManagerConfiguredTest.java
# Fails for various reason (use org.jboss:jboss-vfs:jar:3.2.6.Final)
rm -r core-server/src/test/java/org/glassfish/jersey/server/SecurityContextTest.java \
 core-server/src/test/java/org/glassfish/jersey/server/internal/process/ProxyInjectablesTest.java \
 core-server/src/test/java/org/glassfish/jersey/server/internal/inject/JaxRsInjectablesTest.java \
 core-server/src/test/java/org/glassfish/jersey/server/model/ResourceInfoTest.java
# Exception: Unexpected exception, expected<java.security.AccessControlException> but was<java.lang.AssertionError>
rm -r core-common/src/test/java/org/glassfish/jersey/internal/util/ReflectionHelperTest.java
# Could not find javax.ws.rs-api.
rm -r core-server/src/test/java/org/glassfish/jersey/server/internal/scanning/JarFileScannerTest.java \
 core-server/src/test/java/org/glassfish/jersey/server/internal/scanning/PackageNamesScannerTest.java \
 core-server/src/test/java/org/glassfish/jersey/server/internal/scanning/VFSSchemeResourceFinderTest.java

rm -r test-framework/providers/grizzly2/src/test/java/org/glassfish/jersey/test/grizzly/web/GrizzlyWebInjectionTest.java

# NO test dep org.jmockit:jmockit
rm -r ext/cdi/jersey-cdi1x/src/test/java/org/glassfish/jersey/ext/cdi1x/internal/CdiUtilTest.java \
 core-server/src/test/java/org/glassfish/jersey/server/ResourceConfigTest.java \
 core-client/src/test/java/org/glassfish/jersey/client/ClientRequestTest.java
rm -r ext/cdi/jersey-cdi1x/src/test/java/*
%pom_remove_dep org.glassfish.jersey.connectors:jersey-grizzly-connector media/multipart
rm -r media/multipart/src/test/java/org/glassfish/jersey/media/multipart/internal/MultiPartHeaderModificationTest.java \
 media/multipart/src/test/java/org/glassfish/jersey/media/multipart/internal/FormDataMultiPartReaderWriterTest.java \
 media/multipart/src/test/java/org/glassfish/jersey/media/multipart/MultipartMixedWithApacheClientTest.java \
 media/multipart/src/test/java/org/glassfish/jersey/media/multipart/internal/MultiPartReaderWriterTest.java \
 media/multipart/src/test/java/org/glassfish/jersey/media/multipart/internal/FormDataMultiPartBufferTest.java

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

# Disable modules we cannot build or do not need
%pom_disable_module bom
%pom_disable_module json-jackson1 media
%pom_disable_module json-jettison media
%pom_disable_module json-processing media
%pom_disable_module multipart media
%pom_disable_module sse media
%pom_disable_module containers
%pom_disable_module core-server
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
%pom_disable_module spring3 ext
%pom_disable_module wadl-doclet ext
%pom_disable_module incubator
%pom_disable_module security
sed -i '/rx-client-java8/ d' pom.xml

# Port to older httpcomponents
%pom_xpath_remove "pom:dependency[pom:scope = 'test' ]" connectors/apache-connector
sed -i -e '/setConnectionManagerShared/ d' -e '/CONNECTION_MANAGER_SHARED/ d' \
       -e 's/HostnameVerifier hostnameVerifier = client.getHostnameVerifier()/org.apache.http.conn.ssl.X509HostnameVerifier hostnameVerifier = SSLConnectionSocketFactory.BROWSER_COMPATIBLE_HOSTNAME_VERIFIER/' \
  connectors/apache-connector/src/main/java/org/glassfish/jersey/apache/connector/ApacheConnector.java

# Avoid building the server component
%pom_xpath_remove "pom:dependency[pom:scope = 'test' ]" ext/entity-filtering
%pom_remove_dep :jersey-server ext/entity-filtering
sed -i -e '/ServerScopeProvider/ d' -e '/SecurityEntityFilteringFeature/ d' \
  ext/entity-filtering/src/main/java/org/glassfish/jersey/message/filtering/EntityFilteringFeature.java
for f in ServerScopeProvider SecurityEntityFilteringFeature SecurityServerScopeProvider; do
  rm -f ext/entity-filtering/src/main/java/org/glassfish/jersey/message/filtering/$f.java
done

%mvn_package "org.glassfish.jersey.test-framework:project" test-framework
%mvn_package "org.glassfish.jersey.test-framework.providers:project" test-framework
%mvn_package ":%{pkg_name}-test-framework-core" test-framework 
%mvn_package ":%{pkg_name}-test-framework-provider-bundle" test-framework
%mvn_package ":%{pkg_name}-test-framework-provider-external" test-framework
%mvn_package ":%{pkg_name}-test-framework-provider-grizzly2" test-framework
%mvn_package ":%{pkg_name}-test-framework-provider-inmemory" test-framework
%mvn_package ":custom-enforcer-rules" test-framework
%mvn_package ":memleak-test-common" test-framework
%if %{with jetty}
%mvn_package ":%{pkg_name}-test-framework-provider-jetty" test-framework
%endif
%mvn_package ":%{pkg_name}-test-framework-provider-jdk-http" test-framework
%mvn_package ":%{pkg_name}-test-framework-provider-simple" test-framework
%mvn_package ":%{pkg_name}-test-framework-util" test-framework
# Conflict with org.glassfish.jersey:project
%mvn_file "org.glassfish.jersey.test-framework:project" %{pkg_name}/test-framework-project
%mvn_file "org.glassfish.jersey.test-framework.maven:project" %{pkg_name}/test-framework-maven-project
%mvn_file "org.glassfish.jersey.test-framework.providers:project" %{pkg_name}/test-framework-providers-project
%mvn_file "org.glassfish.jersey.connectors:project" %{pkg_name}/connectors-project
%mvn_file "org.glassfish.jersey.containers:project" %{pkg_name}/containers-project
%mvn_file "org.glassfish.jersey.ext:project" %{pkg_name}/ext-project
%mvn_file "org.glassfish.jersey.ext.cdi:project" %{pkg_name}/ext-cdi-project
%mvn_file "org.glassfish.jersey.ext.rx:project" %{pkg_name}/ext-rx-project
%mvn_file "org.glassfish.jersey.incubator:project" %{pkg_name}/incubator-project
%mvn_file "org.glassfish.jersey.media:project" %{pkg_name}/media-project
%mvn_file "org.glassfish.jersey.security:project" %{pkg_name}/security-project
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x

%mvn_build -f -- -DskipTests=true -Dtest-framework.excluded -Dexamples.excluded
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc README.md
%doc LICENSE.html LICENSE.txt LICENSE-2.0.txt etc/config/copyright.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.html LICENSE.txt LICENSE-2.0.txt etc/config/copyright.txt

%changelog
* Wed Jul 27 2016 Mat Booth <mat.booth@redhat.com> - 2.22.2-1.2
- Disable modules we don't need
- Port to older httpcomponents

* Tue Jul 26 2016 Mat Booth <mat.booth@redhat.com> - 2.22.2-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Thu Feb 18 2016 gil cattaneo <puntogil@libero.it> 2.22.2-1
- update to 2.22.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Orion Poplawski <orion@cora.nwra.com> 2.22.1-2
- Rebuild for osgi-resource-locator change

* Wed Oct 14 2015 gil cattaneo <puntogil@libero.it> 2.22.1-1
- update to 2.22.1

* Sun Oct 04 2015 gil cattaneo <puntogil@libero.it> 2.22-1
- update to 2.22

* Wed Aug 19 2015 gil cattaneo <puntogil@libero.it> 2.21-1
- update to 2.21

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
