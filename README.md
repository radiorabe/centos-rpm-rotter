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

### Running rotter through systemd
`rotter` and `jackd` can be started via the installed systemd service unit
template pairs (and therefore support multiple instances).

To create a rotter and jackd instance pair named `example` and use jackd's
ALSA backend, proceed with the following steps:
```bash
# The name of the rotter and jackd instance pair
instanceName="example"

# Create a service instance override for running jackd under the rotter
# user/group with the alsa backend
mkdir /etc/systemd/system/jackd@${instanceName}.service.d
cat > /etc/systemd/system/jackd@${instanceName}.service.d/override.conf << "EOF"
[Service]
User=rotter
Group=rotter

# Jackd startup options
Environment="JACKD_OPTIONS=-d alsa --device hw:0 --capture --inchannels 2"
EOF

# Enable and start the jackd 'example' instance
systemctl enable jackd@${instanceName}.service
systemctl start jackd@${instanceName}.service
systemctl status jackd@${instanceName}.service

# Enable and start the rotter 'example' instance
systemctl enable rotter@${instanceName}.service
systemctl start rotter@${instanceName}.service
systemctl status rotter@${instanceName}.service
```

The systemd service will also create the necessary recording root directory
located within the rotter instance root directory
<code>/var/lib/rotter/<INSTANCE></code>. Or in other words, the recordings
will be be available at <code>/var/lib/rotter/example</code> in our example.

### Systemd service unit templates explained
The included Systemd service unit templates for `rotter` and `jackd` correlate
with each other and are supposed to be run with the same instance name.

[`jackd@.service`](jackd@.service) is a generic service unit template for
starting one ore more headless `jackd` instances:
* It is a generic jackd service unit template and can be used for other
  use-cases as well (i.e. it's not limited to the rotter usage)
* It sets the required real-time priorities (`LimitRTPRIO=`) and maximum
  locked-in-memory address space (`LimitMEMLOCK=`)
* It starts `jackd` with the dummy backend by default.
* The name of the systemd service instance is used as the jack server name
  (`jackd --name <instance>`), so use `default` as the instance name if you
  would like to use the `default` jack server.
* The unit waits for the `jackd` to be up and running with the help of the
  `jack_wait` command.
* Start-up overrides of possible interest are `User=`/`Group=`,
  `Environment="JACKD_SERVERNAME=%i"` and `Environment="JACKD_OPTIONS=-d dummy"`
  
[`rotter@.service`](rotter@.service) is a service unit template for starting one
ore more `rotter` instances:
* It depends on a `jackd` system service instance unit with the same instance name
  (`BindsTo=jackd@%i.service`)
* It sets the required real-time priorities (`LimitRTPRIO=`) and maximum
  locked-in-memory address space (`LimitMEMLOCK=`)
* It starts `rotter` under the `rotter` system user and group by default
* It conects to a `jackd` server with the same name as the instance by default
* It stores the recorded audio files below `/var/lib/rotter/<instance>` by default
* Startup-up overrides of possible interest are 
  `Environment="ROTTER_ROOT_DIR=/var/lib/rotter/%i"`, `Environment="ROTTER_OPTIONS=-a -j"`
  and `Environment="JACK_DEFAULT_SERVER=%i"`
 
