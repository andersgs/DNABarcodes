#!/bin/sh

#########################################################################################
## install functions ####################################################################
#########################################################################################

#########################################################################################
### Main function #######################################################################
#########################################################################################

main(){
	echo ""
	echo "Script to install dnaBarcodes"
	echo "version 0.1dev"
	echo "(C) 2014 Anders Goncalves da Silva and Rohan H Clarke"
	echo "====================================================="
	echo ""



	debug=false
	py=false #install python
	pe=false #install perl
	mp=false #install macports
	gcc=false #install gcc
	bl=false #install ncbi tools
	pd=false #install phred
	pp=false #install phrap
	po=false #install polyphred
	cs=false #install consed
	all=true #install all
	del=false #clean directories

	while getopts ":dyegbdpocn" optname
		do
			case $optname in
				d)
					debug=true
				;;
				y)
					py=true
					all=false
				;;
				e)
					pe=true
					all=false
				;;
				m)
					mp=true
					all=false
				;;
				g)
					gcc=true
					all=false
				;;
				b)
					bl=true
					all=false
				;;
				d)
					pd=true
					all=false
				;;
				p)
					pp=true
					all=false
				;;
				o)
					po=true
					all=false
				;;
				c)
					cs=true
					all=false
				;;
				n)
					del=true
			esac
		done

##### default versions
	pyversion=2.7
	plversion=5.12
	gcc_version=4.6

#### default install directory for phred/phrap/polyphred/consed
	default_dir=/usr/local/genome

	if [[ "$del" = true ]]
	then
		echo "Cleaning default installation folder..."
		rm -rdf $default_dir
	fi


	check_dir $default_dir
	
# install macports if needed	
	
	if ([[ "$mp" = true ]] || [[ "$all" = true ]]) && [ "$debug" = false ]
	then
		install_port
	elif [[ "$mp" = false ]] && [[ "$debug" = true ]]
	then
		echo "Would install macports here"
	else
		if [ $(command -v port) ]
			then
				echo "Found Macports..."
				port selfupdate
		else
			no_prog_error macports
		fi
	fi
	
# install python 2.7 if needed

	if [[ $(test_version $pyversion python) ]]
	then
		echo "Python installed successfully. Continuing to next step..."
	else
		if ([[ "$py" = true ]] || [[ "$all" = true ]]) && [ "$debug" = false ]
			then
				install_python_mac
		elif [[ "$py" = false ]] && [[ "$debug" = true ]]
		then
			echo "Would install python now"
		else
			if [ ! $(command -v python) ]
				then
					install_python_mac
			else
					no_prog_error python
			fi
		fi
	fi

# install perl 5.12 if needed

	if [[ $(test_version $plversion perl) ]]
	then
		echo "Perl installed successfully. Continuing to next step..."
	else
		if ([[ "$pe" = true ]] || [[ "$all" = true ]]) && [ "$debug" = false ]
			then
				install_perl_mac
		elif [[ "$pe" = false ]] && [[ "$debug" = true ]]
		then
			echo "Would install Perl now"
		else
			if [ ! $(command -v perl) ]
				then
					install_perl_mac
			else
					no_prog_error perl
			fi
		fi
	fi
	
#install ncbi_tools
	if [[ $(command -v blastn) ]]
	then 
		echo "Found NCBI Tools installed... Continuing to next step..."
	else
		if ([[ "$bl" = true ]] || [[ "$all" = true ]]) && [[ "$debug" = false ]]
		then
			ask_install ncbi_tools
			install_ncbi_mac
		elif [[ "$bl" = false ]] && [[ "$debug" = true ]]
		then
			echo "Would install NCBI tools here"
		else
			no_prog_error ncbi_tools
		fi
	fi

#figure gcc before continuing to next step
	if ([[ "$gcc" = true ]] || [[ "$all" = true ]]) && [[ "$debug" = false ]]
	then
		ask_install gcc
		test_gcc_mac
	elif [[ "$gcc" = false ]] && [[ "$debug" = true ]]
	then
		echo "Would install gcc now"
	else
		echo "$gcc and $debug"
		no_prog_error gcc
	fi

#install consed
	if [[ $(command -v consed) ]]
	then
		echo "Consed already installed..."
	else
		if ([[ "$cs" = true ]] || [[ "$all" = true ]]) && [[ "$debug" = false ]]
		then 
			ask_install consed
			install_consed_mac
		elif [[ "$cs" = false ]] && [[ "$debug" = true ]]
		then
			echo "Consed would be installed here"
		else
			no_prog_error consed
		fi
	fi

#install phred
	if [[ $(command -v phred) ]] && [[ $(command -v phd2fasta) ]]
	then
		echo "Found phred and phd2fasta already installed..."
	else
		if ([[ "$pd" = true ]] || [[ "$all" = true ]]) && [[ "$debug" = false ]]
		then
			ask_install phred
			install_phred_mac
		elif [[ "$pd" = false ]] && [[ "$debug" = true ]]
		then
			echo "Phred would be installed here"
		else
			no_prog_error phred
		fi
	fi

#install phrap
	if [[ $(command -v phrap) ]]
	then
		echo "Phrap already installed..."
	else
		if ([[ "$pp" = true ]] || [[ "$all" = true ]]) && [[ "$debug" = false ]]
		then 
			ask_install phrap
			install_phrap_mac
		elif [[ "$pp" = false ]] && [[ "$debug" = true ]]
		then
			echo "Phrap would be installed here"
		else
			no_prog_error phrap
		fi
	fi
	
#install polyphred
	if [[ $(command -v polyphred) ]]
	then
		echo "Polyphred already installed..."
	else
		if ([[ "$po" = true  ]] || [[ "$all" = true ]]) && [[ "$debug" = false ]]
		then 
			ask_install polyphred
			install_polyphred_mac
		elif [[ "$po" = false ]] && [[ "$debug" = true ]]
		then
			echo "Polyphred would be installed here"
		else
			no_prog_error polyphred
		fi
	fi
	
#export some variables

if [[ "$debug" == false ]]
	then
		echo ' ' >> ~/.bash_profile
		echo "#######Inserted by DNABarcodes install script#######" >> ~/.bash_profile
		echo ' ' >> ~/.bash_profile
		echo "export PATH=$default_dir/bin:$PATH" >> ~/.bash_profile
		echo ' ' >> ~/.bash_profile
		echo "export PHRED_PARAMETER_FILE=$default_dir/lib/phredpar.dat" >> ~/.bash_profile
		echo '' >> ~/.bash_profile
		echo "#######End of insert by DNABarcodes install script######" >> ~/.bash_profile
		echo '' >> ~/.bash_profile

	
	exit 0		
}

#########################################################################################
### Aux function #######################################################################
#########################################################################################

#################
### Check if sufficient privileges to install system wide

check_sudo(){
	if [ $EUID != 0 ]
	then
		echo "Please run the program again with sudo:"
		echo "> sudo ./install2.sh"
		exit 1
	fi
}

#################
### Check if default dir is suitable

check_dir(){
	
	echo "Will install Phred/Phrap/PolyPhred/Consed in $1."
	while true; do
		read -p "Enter alternate directory, or press <enter> to accept default: " dir
		if [ ! $dir ]
		then
			echo "Using $1 then"
			if [ ! -d $1 ]
			then
				mkdir -p $1
			fi
			break
		else
			if [ -d $dir ]
			then
				echo "Using $dir then"
				break
			else
				echo "Using $dir then"
				mkdir -p $dir
				default_dir=$dir
				break
			fi
		fi
	done
}



#################
### yes/no function
ask_yesno(){
	while true; do
		read -p "Install $1? [y]es or [n]" yn
		case $yn in
			[Yy]*)
				$2
				;;
			[Nn]*) 
				echo "Please install $1 before continuing"
				exit 1
				;;
			*) 
				echo "Please answer Yes or No."
				;;
			esac
	done
}

################
### test version
test_version(){
	def=$1
	prog=$2
	echo $prog
	local_version=`$prog --version 2>&1 | sed -n 's/.*\([0-9]\.[0-9]\{1,\}\)\.[0-9]\{0,\}.*/\1/p'`
	echo $local_version
	if [ $(echo "$local_version >= $def" | bc) ]
		then
			return 0
	else
		return 1
	fi
}


################
### 
install_port(){
	if [ ! $(command -v port) ]
		then
			ask_install macports
			curl -O http://svn.macports.org/repository/macports/downloads/MacPorts-1.5.0/MacPorts-1.5.0-10.4.dmg
			hdiutil attach MacPorts-1.5.0-10.4.dmg
			sudo installer -verbose -pkg /Volumes/MacPorts-1.5.0/MacPorts-1.5.0.pkg -target /
			sudo port -v selfupdate
			hdiutil detach -verbose /Volumes/MacPorts-1.5.0/
			hash -r	
	else
		echo "Found macports... Continuing to next step..."
	fi
}

################
###  install python
install_python_mac(){
	if [ ! $(command -v port) ]
		then
			ask_install python
			port install python27
			if [ $(command -v /usr/bin/python) ]
			then
				mv /usr/bin/python /usr/bin/python-orig
			fi
			port select --set python python27
			hash -r
	else
		echo "Found python... Continuing to next step..."
	fi
}

################
### install perl
install_perl_mac(){
	if [ ! $(command -v port) ]
		then
		ask_install perl
		port install perl5.12
		if [ $(command -v /usr/bin/perl) ]
		then
			mv /usr/bin/perl /usr/bin/perl-orig
		fi
		#port select --set perl perl512
		hash -r
	else
		echo "Found perl... Continuing to next step..."
	fi
}

################
### install ncbi tools
install_ncbi_mac(){
	echo "Checking for latest version..."
	latest_version=`curl 'ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/' --list-only | grep 'dmg'`
	
	echo "Downloading latest version..."
	curl -O "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/$latest_version"
	
	echo "Unpacking and installing..."
	hdiutil attach $latest_version
	latest=`echo $latest_version | sed 's/\(.\)\.dmg/\1/'`
	pkg=`echo $latest_version | sed 's/\(.\)\.dmg/\+\.pkg/'`
	installer -verbose -pkg /Volumes/$latest/$pkg -target /
	hdiutil detach -verbose /Volumes/$latest/
	hash -r
}

######
### Exit error
no_prog_error(){
	echo "Cannot continue without $1... Exiting now."
	exit 1
}

##########
### ask install
ask_install(){
	read -p "About run script to check/install/upgrade $1... Press <enter> to install, or c to cancel: " ans
	if [ ! $ans ]
		then
			echo "Running script for $1..."
	else
		no_prog_error $1
	fi

}

#########
### test and install gcc if necessary
test_gcc_mac(){
	clang=`eval gcc --version 2>&1 | grep 'clang'`
	if [ ! ${#clang} ]
	then
		echo "Using Apples default compiler"
		echo "You should upgrade"
		echo "Do you wish to upgrade? [y/n]"
		while true
		do
			read ans
			if [ $ans == 'y' ]
			then
				sudo port install gcc46
				sudo port select --set gcc mp-gcc46
				break
			elif [ $ans == 'n' ]
			then
				echo "Sorry, cant proceed."
				echo "A newer version of GCC is needed to successfully install Phred/Phrap/Consed/PolyPhred"
				exit 1
			else
				echo "Must type y or n"
				echo "Press any key to continue..."
				read key
			fi
		done
	else
		gversion=`eval gcc --version 2>&1| sed -n 's/.*\(4.[6,7,8]\).*$/\1/p'`
		if [ $(echo "$gversion >= $gcc_version" | bc) ]
		then
			echo "Your current version of gcc is $gversion, which is => then the required version: $gcc_version"
		else
			echo "Your current version of gcc, $gversion, is not suitable"
			echo "You should upgrade your gcc to version 4.6"
			echo "Do you wish to upgrade? [y/n] "
			while true
			do
				read ans
				if [ $ans == 'y' ]
				then
					sudo port install gcc46
					sudo port select --set gcc mp-gcc46
					break
				elif [ $ans == 'n' ]
				then
					echo "Sorry, cant proceed."
					echo "A newer version of GCC is needed to successfully install Phred/Phrap/Consed/PolyPhred"
					exit 1
				else
					echo "Must type y or n"
					echo "Press any key to continue..."
					read key
				fi
			done
		fi
	fi
			
}

##############
### install phred

install_phred_mac(){
	echo "Checking for Phred package..."
	
	
	if [ -e packages/phred.zip ]
	then
		cd packages/
		unzip -qq phred.zip
		mkdir phred_src
		mkdir phd2fasta_src
		mv phred-dist-020425.c-acd.tar.Z phred_src
		mv phd2fasta-acd-dist.tar.Z phd2fasta_src
		cd phred_src
		tar xZf phred-dist-020425.c-acd.tar.Z
		sed -i .bk 's/-O/-O2 -ansi/' Makefile
		sed -i .bk 's/CC= cc/CC= gcc/' Makefile
		make -s
		if [ -e phred ] && [[ "$debug" = false ]]
		then
			cp phred $defaul_dir/bin
			cp phredpar.dat $default_dir/lib
		elif [ -e phred ] && [ $debug ]
		then
			echo "Compiling phred was successful"
		else
			echo "Compiling phred failed"
			echo "Please double check that you have XCode installed"
			exit 1
		fi
		
		cd ../phd2fasta_src
		tar xZf phd2fasta-acd-dist.tar.Z 
		sed -i .bk 's/-O/-O3/' Makefile 
		sed -i .b 's/cc=cc/cc=gcc/' Makefile
		make -s
		if [ -e phd2fasta ] && [[ "$debug" = false ]]
		then
			cp phd2fasta $default_dir/bin
		elif [ -e phd2fasta ] && [[ "$debug" = true ]]
		then
			echo 'Compiling phd2fasta was successful'
		else
			echo "Compiling phd2fasta failed"
			echo "Please double check that you have XCode installed"
			exit 1
		fi
		cd ..
		rm -rdf phred_src phd2fasta_src
		rm phred-dist*.tar.gz
		cd ..
	else
		echo "Could not find Phred package"
		exit 1
	fi
}

##################
## install phrap

install_phrap_mac(){
	echo "Checking for Phrap package..."

	if [ -e  packages/phrap.tar.gz ]
	then
		cd packages/
		mkdir phrap_src
		cp phrap.tar.gz phrap_src
		cd phrap_src
		tar xzf phrap.tar.gz
		sed -i .b 's/CC= cc/CC= gcc/' makefile
		sed -i .b 's/CFLAGS= -O2/CFLAGS= -O2 -ansi/' makefile
		make -s
		if [ -e phrap ] && [[ "$debug" = false ]]
		then
			echo "Compiling phrap was successfully"
			cp phrap calf_merge cluster cross_match loco phrapview swat $default_dir/bin
			cd ..
			rm -rdf phrap_src
			cd ..
		elif [ -e phrap ] && [[ "$debug" = true ]]
		then
			echo "Compiling phrap was successfully"
			cd ..
			rm -rdf phrap_src
			cd ..
		else
			echo "No success compiling phrap"
		fi
	else
		echo "Could find Phrap packaage"
	fi
}

###################
# install consed

install_consed_mac(){
	echo "Checking for Consed package..."
	if [ -e  packages/consed.tar.gz ]
	then
		cd packages/
		mkdir consed_src
		cp consed.tar.gz consed_src
		cd consed_src
		tar xzf consed.tar.gz
		exe1=consed_mac_intel
		exe2=consed_map_ppc

		err=$(./$exe1 -v 2>&1 | sed -n '/bash/p')

		if [ ${#err} -gt 0 ]
		then
			err=$(./$exe2 -v 2>&1 | sed -n '/bash/p')
			if [ ${#err} -gt 0 ]
			then
				echo "None of the available consed versions work with your system."
				echo "Please try to download a compatible version"
				exit 1
			else
				exe=$exe2
			fi
		else
			exe=$exe1
		fi
		
		if [[ "$debug" = true ]]
		then
			echo "Executable is $exe"
			echo "Location is $default_dir"
			cd ..
			rm -rdf consed_src
			cd ..
		else
			./installConsed.perl $exe $default_dir
			cd ..
			rm -rdf consed_src
			cd ..
		fi
		
	else
		echo "Could not find the consed package"
		echo "Please make sure to download it before continuing"
		exit 1
	fi
}

install_polyphred_mac(){
	echo "Checking for PolyPhred package..."
	if [ -e packages/polyphred.tar.gz ]
	then
		cd packages/
		tar xzf polyphred.tar.gz
		poly_dir=`ls | grep 'polyphred-'`
		
		if [[ "$debug" = true ]]
		then
			echo "Polyphred dir is $poly_dir"
		else
			cd $poly_dir/bin
			cp * $default_dir/bin
		fi
		
		cd ..
		rm -rdf $poly_dir
		cd ..
		echo "Polyphred installed successfully"
	else
		echo "Could not find the polyphred package"
		echo "Please make sure to download it before continuing"
		exit 1	
	fi
}

edit_polyphred(){

	sed -n 's/\#\(\$szPhredParameterFile = \$szConsedHome \. .*\)/\1/p' phredPhrap.pl
	sed -n 's/\(^$niceExe = \).*/\1"\/bin\/usr\/nice"/p' phredPhrap.pl
	sed -n 's/\(^$bUsingPolyPhred = \).*/\11;/p' phredPhrap.pl
}