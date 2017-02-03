%global pypi_name PuLP
%global module_name pulp

Name:           python-%{pypi_name}
Version:        1.6.1
Release:        2%{?dist}
Summary:        LP modeler written in Python

License:        MIT
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{pypi_name}; echo ${n:0:1})/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       coin-or-Cbc
Conflicts:      python-pulp-common

%global _description \
PuLP is an LP modeler written in python. PuLP can generate MPS or LP files\
and call GLPK, COIN CLP/CBC, CPLEX, and GUROBI to solve linear problems.

%description %{_description}

%package -n	python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
Requires:       python2-pyparsing

%description -n python2-%{pypi_name} %{_description}

#Python 2 version.

%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
Requires:       python3-pyparsing

%description -n python3-%{pypi_name} %{_description}

#Python 3 version.

%prep
%autosetup -n %{pypi_name}-%{version}
# removing interpreter from files in site packages
sed -i '1{/^#!/d;}' src/%{module_name}/pulp.py
sed -i '1{/^#!/d;}' src/%{module_name}/amply.py

# Upstream has bin example deps in their
# repo, we need to remove these from the
# source and rely on Requires: coin-or-Cbc

# remove solverdir, it has the bin files
rm -rf src/%{module_name}/solverdir/
# remove refs to solverdir
sed -i '/solverdir/d' setup.py
# fix the python syntax after the solverdir delete
sed -i '/packages/ s/$/ ],/' setup.py

# Remove bundled egg-info
rm -r src/%{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt

%build
%py2_build
%py3_build

%install
%py2_install

# remove the bin files, they're just for development
rm %{buildroot}%{_bindir}/pulptest
rm %{buildroot}%{_bindir}/pulpdoctest

%files -n python2-%{pypi_name}
%license LICENSE
%{python2_sitelib}/pulp/
%{python2_sitelib}/%{pypi_name}-*.egg-info/

%files -n python3-%{pypi_name}
%license LICENSE
#{python3_sitelib}/pulp/
#%{python3_sitelib}/%{pypi_name}-*.egg-info/

%changelog
* Mon Dec 19 2016 Dan Radez <dradez@redhat.com> - 1.6.1-2
- Initial Packaging - Picking up package review from Marcos
* Tue Sep 27 2016 Marcos Fermin Lobo <lobo@lukos.org> - 1.6.1-1
- First RPM
