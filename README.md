# centos-rpm-rotter
CentOS 7 RPM Specfile for Rotter

# centos-rpm-rotter
CentOS 7 RPM Specfile for [Rotter](https://www.aelius.com/njh/rotter/)
(Recording of Transmission / Audio Logger for JACK) which is part of
[Radio Bern RaBe's Audio Packages for Enterprise Linux (RaBe
APEL)](https://build.opensuse.org/project/show/home:radiorabe:audio).

## Usage
There is a pre-built binary packages for CentOS 7 available on [RaBe APEL
package
repository](https://build.opensuse.org/project/show/home:radiorabe:audio),
which can be installed as follows:

```bash
# Add EPEL repository
yum install epel-release

# Add RaBe APEL repository
curl -o /etc/yum.repos.d/home:radiorabe:audio.repo \
     http://download.opensuse.org/repositories/home:/radiorabe:/audio/CentOS_7/home:radiorabe:audio.repo
 
# Install rotter
yum install rotter
```
