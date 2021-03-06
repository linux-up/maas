Summary:	Multicast address allocation server
Summary(pl.UTF-8):	Serwer przydziału adresów multicastowych
Name:		maas
Version:	0.1
Release:	3
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/malloc/%{name}-%{version}.tar.gz
# Source0-md5:	3e27bb1d618fa7f232bee26f9461c951
Source1:	%{name}_manual.pdf
# Source1-md5:	e526a23cabaa9c483a0a0fd9a92ec74b
Source2:	%{name}d.init
Source3:	%{name}d.sysconfig
URL:		http://malloc.sourceforge.net
BuildRequires:	autoconf
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(maasd)
Provides:	user(maasd)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MAAS is multicast address allocation server using MADCAP and AAP
protocols.

%description -l pl.UTF-8
MAAS to serwer przydziału adresów multicastowych wykorzystujący
protokoły MADCAP i AAP.

%prep
%setup -q

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/%{name},/etc/rc.d/init.d,/etc/sysconfig}

install src/maasd $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} .
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/maasd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/maasd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 69 maasd
%useradd -u 69 -d /usr/share/empty -s /bin/false -c "MAAS User" -g maasd maasd

%post
/sbin/chkconfig --add maasd
if [ -r /var/lock/subsys/maasd ]; then
	/etc/rc.d/init.d/maasd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/maasd start\" to start MAAS daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/maasd ]; then
		/etc/rc.d/init.d/maasd stop >&2
	fi
	/sbin/chkconfig --del maasd
fi

%postun
if [ "$1" = "0" ]; then
	%userremove maasd
	%groupremove maasd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS %{name}_manual.pdf src/*.conf
%attr(755,root,root) %{_sbindir}/*
%{_sysconfdir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
