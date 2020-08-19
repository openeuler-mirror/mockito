#!/bin/bash -ex

VERSION=2.23.9
SRCDIR=mockito-${VERSION}

git clone https://github.com/mockito/mockito.git ${SRCDIR}
pushd $SRCDIR
git archive --format=tar --prefix=${SRCDIR}/ v${VERSION} > ../${SRCDIR}.tar
popd

rm -rf ${SRCDIR}

tar -xf ${SRCDIR}.tar
rm ${SRCDIR}.tar
pushd ${SRCDIR}
rm -rf `find -name *.jar` gradlew gradlew.bat src/javadoc
popd

tar -cvJf mockito-${VERSION}.tar.xz ${SRCDIR}
