from AeViz.simulation.methods import *
from AeViz.utils.files.file_utils import load_file
from AeViz.units.aeseries import aeseries
from AeViz.units.aerray import aerray
from AeViz.units import u

"""
Function to load and process log files from a simulation.
These functions are not meant to be used standalone, but rather to be
imported into the Simulation class.
"""

## -----------------------------------------------------------------
## GLOBAL DATA
## -----------------------------------------------------------------

@smooth
@derive
@subtract_tob
def global_neutrino_luminosity(self, tob_corrected=True,
                               comp:Literal['nue', 'nua', 'nux']='all',
                               **kwargs):
    """
    aeseries
    luminosity flux nue  5: number luminosity flux nue
    luminosity flux nua  6: number luminosity flux nua
    luminosity flux nux  7: number luminosity flux nux
    """
    nu_tmp = load_file(self._Simulation__log_path,
                       self._Simulation__integrated_nu_path)
    time = aerray(nu_tmp[:,2], u.s, 'time', r'$t$', None, [0, nu_tmp[-1, 2]], False)
    if comp == 'all':
        return [aeseries(
                        aerray(nu_tmp[:, 38], u.erg / u.s, 'Lnue',
                            r'$L_\mathrm{\nu_e}$', None, [0, 1e53]),
                            time=time),
                aeseries(
                        aerray(nu_tmp[:, 39], u.erg / u.s, 'Lnua',
                            r'$L_\mathrm{\overline{\nu}_e}$', None, [0, 1e53]),
                            time=time.copy()),
                aeseries(
                        aerray(nu_tmp[:, 40] / 4, u.erg / u.s, 'Lnux',
                            r'$L_\mathrm{\nu_x}$', None, [0, 1e53]),
                            time=time.copy()),
                ]
    elif comp == 'nua':
        return aeseries(
                        aerray(nu_tmp[:, 39], u.erg / u.s, 'Lnua',
                            r'$L_\mathrm{\overline{\nu}_e}$', None, [0, 1e53]),
                            time=time.copy())
    elif comp == 'nue':
        return aeseries(
                        aerray(nu_tmp[:, 38], u.erg / u.s, 'Lnue',
                            r'$L_\mathrm{\nu_e}$', None, [0, 1e53]),
                            time=time)
    elif comp == 'nux':
        return aeseries(
                        aerray(nu_tmp[:, 40] / 4, u.erg / u.s, 'Lnux',
                            r'$L_\mathrm{\nu_x}$', None, [0, 1e53]),
                            time=time.copy())

@subtract_tob
def global_neutrino_number_luminosity(self, tob_corrected=True,
                                      comp:Literal['nue', 'nua', 'nux']='all',
                                      **kwargs):
    """
    aeseries
    number luminosity flux nue
    number luminosity flux nua
    number luminosity flux nux
    """
    nu_tmp = load_file(self._Simulation__log_path,
                       self._Simulation__integrated_nu_path)
    time = aerray(nu_tmp[:,2], u.s, 'time', r'$t$', None, [0, nu_tmp[-1, 2]], False)
    if comp == 'all':
        return [aeseries(
                        aerray(nu_tmp[:, 35], u.dimensionless_unscaled / u.s,
                            'Lnue',
                            r'$N_\mathrm{\nu_e}$', None, [0, 1e55]),
                            time=time),
                aeseries(
                        aerray(nu_tmp[:, 36], u.dimensionless_unscaled / u.s,
                            'Lnumnua',
                            r'$N_\mathrm{\overline{\nu}_e}$', None, [0, 1e55]),
                            time=time.copy()),
                aeseries(
                        aerray(nu_tmp[:, 37] / 4, u.dimensionless_unscaled / u.s,
                            'Lnumnux',
                            r'$N_\mathrm{\nu_x}$', None, [0, 1e55]),
                            time=time.copy()),
        ]
    elif comp == 'nua':
        return aeseries(
                        aerray(nu_tmp[:, 36], u.dimensionless_unscaled / u.s,
                            'Lnumnua',
                            r'$N_\mathrm{\overline{\nu}_e}$', None, [0, 1e55]),
                            time=time.copy())
    elif comp == 'nue':
        return aeseries(
                        aerray(nu_tmp[:, 35], u.dimensionless_unscaled / u.s,
                            'Lnue',
                            r'$N_\mathrm{\nu_e}$', None, [0, 1e55]),
                            time=time)
    elif comp == 'nux':
        return aeseries(
                        aerray(nu_tmp[:, 37] / 4, u.dimensionless_unscaled / u.s,
                            'Lnumnux',
                            r'$N_\mathrm{\nu_x}$', None, [0, 1e55]),
                            time=time.copy())

@smooth
@derive
def global_neutrino_mean_energies(self, tob_corrected=True,
                                  comp:Literal['nue', 'nua', 'nux']='all',
                                  **kwargs):
    """
    list of aeseries
    1: mean energy nue  
    2: mean energy nua  
    3: mean energy nux  
    """
    nu_lum = self.global_neutrino_luminosity(tob_corrected)
    nu_num = self.global_neutrino_number_luminosity(tob_corrected)
    mean_ene = [(nu_lum[i] / nu_num[i]).to(u.MeV) for i in range(len(nu_lum))]
    for me, nm, lb in zip(mean_ene, ['Enue', 'Enua', 'Enux'],
                          [r'$\langle E_{\nu_\mathrm{e}}\rangle$',
                           r'$\langle E_{\overline{\nu}_\mathrm{e}}\rangle$',
                           r'$\langle E_{\nu_\mathrm{x}}\rangle$']):
        me.data.set(name=nm, limits=[0,30], label=lb)
    if comp == 'all': 
        return mean_ene
    elif comp == 'nue':
        return mean_ene[0]
    elif comp == 'nua':
        return mean_ene[1]
    elif comp == 'nux':
        return mean_ene[2]

@smooth
@derive
@subtract_tob
def total_mass(self, tob_corrected=True, **kwargs):
    """
    Aeseries with mass in solar masses
    """
    file = load_file(self._Simulation__log_path, self._Simulation__rho_max_path)
    M = aerray(file[:, 4], u.g, 'mtot', r'$M_\mathrm{tot}$', limits=[0, 10]).to(u.M_sun)
    time = aerray(file[:, 2], u.s, 'time', r'$t$', None, [0, file[-1, 2]], False)
    return aeseries(M, time=time)

@smooth
@derive
@subtract_tob
def global_rho(self, tob_corrected=True, comp:Literal['max', 'min']='max',
               **kwargs):
    """
    indices
    1: time
    2: rho max
    """
    rho = load_file(self._Simulation__log_path, self._Simulation__rho_max_path)
    time = aerray(rho[:,2], u.s, 'time', r'$t$', None, [0, rho[-1, 2]], False)       
    if comp == 'max':
        return aeseries(
            aerray(rho[:, 3], u.g / u.cm ** 3, 'rho_max', r'$\rho_\mathrm{max}$',
                   'viridis', [1e4, 1e15], True),
            time=time
        )
    elif comp == 'min':
        return aeseries(
            aerray(rho[:, 5], u.g / u.cm ** 3, 'rho_max', r'$\rho_\mathrm{max}$',
                   'viridis', [1e-3, 1e2], True),
            time=time
        )

@smooth
@derive
@subtract_tob
def global_Ye(self, tob_corrected=True, comp:Literal['max', 'min', 'cent']='cent',
              **kwargs):
    Ye = load_file(self._Simulation__log_path, self._Simulation__rho_max_path)
    time = aerray(Ye[:,2], u.s, 'time', r'$t$', None, [0, Ye[-1, 2]], False)
    if comp == 'max':
        return aeseries(
            aerray(Ye[:, 6], u.dimensionless_unscaled, 'Yemax',
                   r'$Y_\mathrm{e,max}$', None, [0, 1.0], False),
            time = time
        )
    elif comp == 'min':
        return aeseries(
                aerray(Ye[:, 7], u.dimensionless_unscaled, 'Yemin',
                       r'$Y_\mathrm{e,min}$', None, [0, 0.5], False),
                time = time
            )
    elif comp == 'cent':
        return aeseries(
                aerray(Ye[:, 8], u.dimensionless_unscaled, 'Yecent',
                       r'$Y_\mathrm{e,cent}$', None, [0, 0.5], False),
                time = time
            )

@smooth
@derive
@subtract_tob
def global_temperature(self, tob_corrected=True, comp:Literal['max', 'min',
                                                              'cent']='max',
              **kwargs):
    T = load_file(self._Simulation__log_path, self._Simulation__erg_data)
    time = aerray(T[:,2], u.s, 'time', r'$t$', None, [0, T[-1, 2]], False)
    if comp == 'max':
        return aeseries(
            aerray(T[:, -6], u.MeV, 'Tmax',
                   r'$T_\mathrm{max}$', None, [0, 40], False),
            time = time
        )
    elif comp == 'min':
        return aeseries(
                aerray(T[:, -7], u.MeV, 'Tmin',
                       r'$T_\mathrm{min}$', None, [0, 1], False),
                time = time
            )
    elif comp == 'cent':
        return aeseries(
                aerray(T[:, -2], u.MeV, 'Tcent',
                       r'$T_\mathrm{cent}$', None, [0, 40], False),
                time = time
            )

@smooth
@derive
@subtract_tob
def global_entropy(self, tob_corrected=True, comp:Literal['max', 'min',
                                                              'cent']='max',
              **kwargs):
    T = load_file(self._Simulation__log_path, self._Simulation__erg_data)
    time = aerray(T[:,2], u.s, 'time', r'$t$', None, [0, T[-1, 2]], False)
    if comp == 'max':
        return aeseries(
            aerray(T[:, -4], u.kBol / u.bry, 'entropymax',
                   r'$s_\mathrm{max}$', None, [0, 100], False),
            time = time
        )
    elif comp == 'min':
        return aeseries(
                aerray(T[:, -5], u.kBol / u.bry, 'entropymin',
                       r'$s_\mathrm{min}$', None, [0, 1], False),
                time = time
            )
    elif comp == 'cent':
        return aeseries(
                aerray(T[:, -3], u.kBol / u.bry, 'entropycent',
                       r'$s_\mathrm{cent}$', None, [0, 5], False),
                time = time
            )
        
@smooth
@derive
@subtract_tob
def global_gas_pressure(self, tob_corrected=True, comp:Literal['max', 'min']='max',
              **kwargs):
    T = load_file(self._Simulation__log_path, self._Simulation__erg_data)
    time = aerray(T[:,2], u.s, 'time', r'$t$', None, [0, T[-1, 2]], False)
    if comp == 'max':
        return aeseries(
            aerray(T[:, -8], u.Ba, 'gas_pressuremax',
                   r'$P_\mathrm{gas,max}$', None, [1e25, 1e34], True),
            time = time
        )
    elif comp == 'min':
        return aeseries(
                aerray(T[:, -9], u.Ba, 'gas_pressuremin',
                       r'$P_\mathrm{gas,min}$', None, [1e-5, 1e1], True),
                time = time
            )

@smooth
@derive
@subtract_tob
def global_radial_velocity(self, tob_corrected=True, **kwargs):
    v = load_file(self._Simulation__log_path, self._Simulation__vel_data)
    time = aerray(v[:,2], u.s, 'time', r'$t$', None, [0, v[-1, 2]], False)
    return aeseries(
            aerray(v[:, -3], u.cm / u.s, 'vrmax',
                   r'$v_\mathrm{r,max}$', None, [-1e10, 5e10], True),
            time = time
        )

@smooth
@derive
@subtract_tob
def global_theta_velocity(self, tob_corrected=True, **kwargs):
    v = load_file(self._Simulation__log_path, self._Simulation__vel_data)
    time = aerray(v[:,2], u.s, 'time', r'$t$', None, [0, v[-1, 2]], False)
    return aeseries(
            aerray(v[:, -2], u.cm / u.s, 'vthetamax',
                   r'$v_{\theta,\mathrm{max}}$', None, [-1e10, 5e10], True),
            time = time
        )

@smooth
@derive
@subtract_tob
def global_theta_velocity(self, tob_corrected=True, **kwargs):
    v = load_file(self._Simulation__log_path, self._Simulation__vel_data)
    time = aerray(v[:,2], u.s, 'time', r'$t$', None, [0, v[-1, 2]], False)
    return aeseries(
            aerray(v[:, -1], u.cm / u.s, 'vphimax',
                   r'$v_{\phi,\mathrm{max}}$', None, [-1e10, 5e10], True),
            time = time
        )
   
@smooth
@derive
@subtract_tob
def global_rotational_energy(self, tob_corrected=True, **kwargs):
    """
    1: time
    2: total rotational energy
    """
    en = load_file(self._Simulation__log_path, self._Simulation__erg_data)
    time = aerray(en[:, 2], u.s, 'time', r'$t$', None, [0, en[-1, 2]], False)
    return aeseries(
        aerray(en[:, 10], u.erg, 'Erottot',
               r'$E_\mathrm{rot,tot}$', None, [1e49, 1e53], True),
        time=time
    )

@smooth
@derive
@subtract_tob
def global_internal_energy(self, tob_corrected=True, **kwargs):
    en = load_file(self._Simulation__log_path, self._Simulation__erg_data)
    time = aerray(en[:, 2], u.s, 'time', r'$t$', None, [0, en[-1, 2]], False)
    return aeseries(
        aerray(en[:, 4], u.erg, 'internal_energy',
                  r'$E_{\mathrm{int,max}}$', 'nipy_spectral', [1e24, 1e35], log=True),
        time=time
    )

@smooth
@derive
@subtract_tob
def global_magnetic_energy(self, comp: Literal['tot', 'pol', 'tor', 'r',
                                               'th', 'ph']='tot',
                           tob_corrected=True, **kwargs):
    en = load_file(self._Simulation__log_path, self._Simulation__mag_data)
    time = aerray(en[:, 2], u.s, 'time', r'$t$', None, [0, en[-1, 2]], False)
    if comp == 'tot':
        return aeseries(
            aerray(en[:, 3], u.erg, 'magnetic_energy',
                    r'$E_{\mathrm{mag,tot}}$', 'nipy_spectral', [1e30, 1e51],
                    log=True),
            time=time
        )
    elif comp == 'pol':
        return aeseries(
            aerray(en[:, 4] + en[:, 5], u.erg, 'magnetic_energy',
                    r'$E_{\mathrm{mag,pol}}$', 'nipy_spectral', [1e30, 1e51],
                    log=True),
            time=time
        )
    elif comp == 'tor':
        return aeseries(
            aerray(en[:, 6], u.erg, 'magnetic_energy',
                    r'$E_{\mathrm{mag,tor}}$', 'nipy_spectral', [1e30, 1e51],
                    log=True),
            time=time
        )
    elif comp == 'r':
        return aeseries(
            aerray(en[:, 4], u.erg, 'magnetic_energy',
                    r'$E_{\mathrm{mag},r}$', 'nipy_spectral', [1e30, 1e51],
                    log=True),
            time=time
        )
    elif comp == 'th':
        return aeseries(
            aerray(en[:, 5], u.erg, 'magnetic_energy',
                    r'$E_{\mathrm{mag},\theta}$', 'nipy_spectral', [1e30, 1e51],
                    log=True),
            time=time
        )
    elif comp == 'ph':
        return aeseries(
            aerray(en[:, 6], u.erg, 'magnetic_energy',
                    r'$E_{\mathrm{mag},\phi}$', 'nipy_spectral', [1e30, 1e51],
                    log=True),
            time=time
        )
        
@smooth
@derive
@subtract_tob
def global_kinetic_energy(self, comp: Literal['tot', 'r', 'th', 'ph']='tot',
                           tob_corrected=True, **kwargs):
    en = load_file(self._Simulation__log_path, self._Simulation__erg_data)
    time = aerray(en[:, 2], u.s, 'time', r'$t$', None, [0, en[-1, 2]], False)
    if comp == 'tot':
        return aeseries(
            aerray(en[:, 7], u.erg, 'kinetic_energy',
                    r'$E_{\mathrm{kin,tot}}$', 'nipy_spectral', [1e30, 1e51],
                    log=True),
            time=time
        )
    elif comp == 'r':
        return aeseries(
            aerray(en[:, 8], u.erg, 'kinetic_energy',
                    r'$E_{\mathrm{kin},r}$', 'nipy_spectral', [1e30, 1e51],
                    log=True),
            time=time
        )
    elif comp == 'th':
        return aeseries(
            aerray(en[:, 9], u.erg, 'kinetic_energy',
                    r'$E_{\mathrm{kin},\theta}$', 'nipy_spectral', [1e30, 1e51],
                    log=True),
            time=time
        )
    elif comp == 'ph':
        return aeseries(
            aerray(en[:, 10], u.erg, 'kinetic_energy',
                    r'$E_{\mathrm{kin},\phi}$', 'nipy_spectral', [1e30, 1e51],
                    log=True),
            time=time
        )