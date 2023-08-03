FROM openjdk:alpine
VOLUME /tmp
ADD spring-petclinic-server/target/petclinic.jar petclinic.jar
RUN sh -c 'touch /petclinic.jar'
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-Dserver.port=8086","-jar","/petclinic.jar"]
