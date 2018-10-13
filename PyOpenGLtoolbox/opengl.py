# coding=utf-8
"""
PYOPENGL-TOOLBOX OPENGL_LIB
Manage OpenGL libraries, init system.

MIT License
Copyright (c) 2018 Pablo Pizarro R.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Library imports
from __future__ import print_function
from PyOpenGLtoolbox.utils import print_gl_error
from OpenGL.GLU import gluPerspective as _gluPerspective

# noinspection PyPep8Naming
import OpenGL.GL as _gl

# Constants
_DEFAULT_AMBIENT_COLOR = [0.2, 0.2, 0.2, 1.0]
_DEFAULT_BGCOLOR = [0.0, 0.0, 0.0, 1.0]
_DEFAULT_BGDEPTH = 1.0
_DEFAULT_CONSTANT_ATTENUATION = 1.0
_DEFAULT_DIFFUSE_COLOR = [0.8, 0.8, 0.8, 1.0]
_DEFAULT_LINEAR_ATTENUATION = 0.0
_DEFAULT_QUADRATIC_ATTENUATION = 0.0
_DEFAULT_SPECULAR_COLOR = [1.0, 1.0, 1.0, 1.0]
_DEFAULT_SPOT_CUTOFF = 180.0
_DEFAULT_SPOT_DIRECTION = [0.0, 0.0, -1.0, 1.0]
_DEFAULT_SPOT_EXPONENT = 1.0
_OPENGL_CONFIGS = [False]
_SPOT_DIRECTION_ALL = [1.0, 1.0, 1.0, 1.0]


def init_gl(antialiasing=True, bgcolor=None, bgdepth=_DEFAULT_BGDEPTH, depth=True, lighting=False,
            materialcolor=True, normalized=True, numlights=0, perspectivecorr=False, polyfonfillmode=True, smooth=True,
            surffill=True, textures=False, transparency=False, verbose=False, version=False):
    """
    Init opengl, params

    antialiasing=true/false (activa el antialiasing, true por defecto)
    bgcolor=color de fondo
    bgdepth=profundidad de dibujo
    depth=true/false (activa el depth map, true por defecto)
    lighting=true/false (activa la iluminacion, false por defecto)
    materialcolor=true/false (activa el color natural de los materiales, true por defecto)
    normalized=true/false (normaliza las normales, true por defecto)
    numlights=1..9 (indica el numero de luces a activar, 0 por defecto)
    perspectivecorr=true/false (activa la correccion de perspectiva, false por defecto)
    polygonfillmode=true/false (indica el rellenar las superficies, true por defecto)
    smooth=true/false (activa el dibujado suave, true por defecto)
    surffil=true/false (activa el rellenado de superficies, true por defecto)
    textures=true/false (activa las texturas, false por defecto)
    transparency=true/false (activa la transparencia de los modelos, true por defecto)
    verbose=true/false (activa el logging, false por defecto)
    version=true/false (imprime la version en pantalla de OpenGL, false por defecto)
    """

    if bgcolor is None:
        bgcolor = _DEFAULT_BGCOLOR

    def log(msg):
        """
        Print a message on screen.

        :param msg: Message
        :type msg: basestring
        """
        if verbose:
            print('[GL] {0}'.format(msg))

    def log_info(msg):
        """
        Print information on screen
        :param msg:
        :return:
        """
        print('[GL-INFO] {0}'.format(msg))

    log('Init OPENGL')

    # Print OpenGL version
    if version:
        log_info('OpenGL version {0}'.format(_gl.glGetString(_gl.GL_VERSION)))
        log_info('GPU {0}'.format(_gl.glGetString(_gl.GL_VENDOR)))
        log_info('Renderer {0}'.format(_gl.glGetString(_gl.GL_RENDERER)))
        log_info('SLSL version {0}'.format(_gl.glGetString(_gl.GL_SHADING_LANGUAGE_VERSION)))
        log_info('Extensions {0}'.format(_gl.glGetString(_gl.GL_EXTENSIONS)))

    # Set background clear color
    if bgcolor is not None:
        log('Clear color set: {0}'.format(bgcolor))
        _gl.glClearColor(*bgcolor)
    else:
        log('Clear color set default')
        _gl.glClearColor(*_DEFAULT_BGCOLOR)

    # Set clear depth color
    if bgdepth is not None:
        log('Clear depth color set: {0}'.format(bgdepth))
        _gl.glClearDepth(bgdepth)
    else:
        log('Clear depth color set default')
        _gl.glClearDepth(_DEFAULT_BGDEPTH)

    # Enable transparency
    if transparency:
        log('Transparency enabled')
        _gl.glEnable(_gl.GL_BLEND)
        _gl.glBlendFunc(_gl.GL_SRC_ALPHA, _gl.GL_ONE_MINUS_SRC_ALPHA)

    # Smooth
    if smooth:
        log('Enable SMOOTH shade model')
        _gl.glShadeModel(_gl.GL_SMOOTH)

    # Depth test
    if depth:
        log('Enable depth test')
        _gl.glEnable(_gl.GL_DEPTH_TEST)
        _gl.glDepthFunc(_gl.GL_LEQUAL)

    # Antialiasing
    if antialiasing:
        log('Antialiasing enabled')
        _gl.glHint(_gl.GL_POLYGON_SMOOTH_HINT, _gl.GL_NICEST)

    # Enabled normalized normal
    if normalized:
        log('Normalized normal enabled')
        _gl.glEnable(_gl.GL_NORMALIZE)

    # Enable offset fill
    if surffill:
        log('Enabled polygon offset fill')
        _gl.glEnable(_gl.GL_POLYGON_OFFSET_FILL)

    # Enable lighting
    if lighting:
        log('Enable lighting')
        _gl.glEnable(_gl.GL_LIGHTING)
        if numlights > 0:
            for light in range(numlights):
                log('Light {0} enabled'.format(light))
                eval('_gl.glEnable(_gl.GL_LIGHT{0})'.format(light))
        _OPENGL_CONFIGS[0] = True

    # Polygon fill mode
    if polyfonfillmode:
        log('Enabled polygoon fill by both sides')
        _gl.glPolygonMode(_gl.GL_FRONT_AND_BACK, _gl.GL_FILL)

    # Enable color material
    if materialcolor:
        log('Enabled color material')
        _gl.glEnable(_gl.GL_COLOR_MATERIAL)

    # Enable perspective correction
    if perspectivecorr:
        log('Enabled pespective correction')
        _gl.glHint(_gl.GL_PERSPECTIVE_CORRECTION_HINT, _gl.GL_NICEST)

    # Enable textures
    if textures:
        log('Textures enabled')
        _gl.glEnable(_gl.GL_TEXTURE_2D)
        _gl.glLightModeli(_gl.GL_LIGHT_MODEL_COLOR_CONTROL, _gl.GL_SEPARATE_SPECULAR_COLOR)

    log('OpenGL init finished')


def clear_buffer():
    """
    Clear buffer
    :return:
    """
    _gl.glClear(_gl.GL_COLOR_BUFFER_BIT | _gl.GL_DEPTH_BUFFER_BIT)


def reshape(w, h, fov=60, nearplane=10, farplane=10000):
    """
    Reshape OpenGL window
    :param w: Window width
    :param h: Window height
    :param fov: Field of view
    :param nearplane: Near plane
    :param farplane: Far plane
    :return:
    """
    h = max(h, 1)
    _gl.glLoadIdentity()

    # Create viewport
    _gl.glViewport(0, 0, w, h)
    _gl.glMatrixMode(_gl.GL_PROJECTION)

    # Create perspective camera
    _gluPerspective(fov, float(w) / float(h), nearplane, farplane)

    # Set model mode
    _gl.glMatrixMode(_gl.GL_MODELVIEW)
    _gl.glLoadIdentity()


def init_light(light=None, ambient=None, constant_att=_DEFAULT_CONSTANT_ATTENUATION,
               diffuse=None, linear_att=_DEFAULT_LINEAR_ATTENUATION,
               quad_att=_DEFAULT_QUADRATIC_ATTENUATION, specular=None,
               spot_cutoff=_DEFAULT_SPOT_CUTOFF, spot_direction=None,
               spot_exponent=_DEFAULT_SPOT_EXPONENT):
    """
    Set light properties.

    :param light: Light OpenGL type GL_LIGHT{n}, n=0..8
    :param ambient: Ambient color
    :param constant_att: Constant attenuation
    :param diffuse: Diffuse color
    :param linear_att: Linear attenuation
    :param quad_att: Quadratic attenuation
    :param specular: Specular color
    :param spot_cutoff: Spot cutoff value
    :param spot_direction: Spot direction value
    :param spot_exponent: Spot exponent value
    :type light: int
    :type ambient: list
    :type constant_att: float, int
    :type diffuse: list
    :type linear_att: float, int
    :type quad_att: float, int
    :type specular: list
    :type spot_cutoff: float, int
    :type spot_direction: float, int
    :type spot_exponent: float, int
    """

    # Checks
    if spot_direction is None:
        spot_direction = _DEFAULT_SPOT_DIRECTION
    if specular is None:
        specular = _DEFAULT_SPECULAR_COLOR
    if diffuse is None:
        diffuse = _DEFAULT_DIFFUSE_COLOR
    if ambient is None:
        ambient = _DEFAULT_AMBIENT_COLOR
    if light is None:
        print_gl_error('Light cannot be None')

    # Ambient color
    if ambient is not None:
        _gl.glLightfv(light, _gl.GL_AMBIENT, ambient)
    else:
        _gl.glLightfv(light, _gl.GL_AMBIENT, _DEFAULT_AMBIENT_COLOR)

    # Diffuse color
    if diffuse is not None:
        _gl.glLightfv(light, _gl.GL_DIFFUSE, diffuse)
    else:
        _gl.glLightfv(light, _gl.GL_DIFFUSE, _DEFAULT_DIFFUSE_COLOR)

    # Specular color
    if specular is not None:
        _gl.glLightfv(light, _gl.GL_SPECULAR, specular)
    else:
        _gl.glLightfv(light, _gl.GL_SPECULAR, _DEFAULT_SPECULAR_COLOR)

    # Cutoff
    if spot_cutoff is not None:
        _gl.glLightfv(light, _gl.GL_SPOT_CUTOFF, spot_cutoff)
    else:
        _gl.glLightfv(light, _gl.GL_SPOT_CUTOFF, _DEFAULT_SPOT_CUTOFF)

    # Exponent
    if spot_exponent is not None:
        _gl.glLightfv(light, _gl.GL_SPOT_EXPONENT, spot_exponent)
    else:
        _gl.glLightfv(light, _gl.GL_SPOT_EXPONENT, _DEFAULT_SPOT_EXPONENT)

    # Spot direction
    if spot_direction is not None:
        _gl.glLightfv(light, _gl.GL_SPOT_DIRECTION, spot_direction)
    else:
        _gl.glLightfv(light, _gl.GL_SPOT_DIRECTION, _DEFAULT_SPOT_DIRECTION)

    # Constant attenuation factor
    if constant_att is not None:
        _gl.glLightfv(light, _gl.GL_CONSTANT_ATTENUATION, constant_att)
    else:
        _gl.glLightfv(light, _gl.GL_CONSTANT_ATTENUATION, _DEFAULT_CONSTANT_ATTENUATION)

    # Lineal attenuation factor
    if linear_att is not None:
        _gl.glLightfv(light, _gl.GL_LINEAR_ATTENUATION, linear_att)
    else:
        _gl.glLightfv(light, _gl.GL_LINEAR_ATTENUATION, _DEFAULT_LINEAR_ATTENUATION)

    # Quadratic attenuation
    if quad_att is not None:
        _gl.glLightfv(light, _gl.GL_QUADRATIC_ATTENUATION, quad_att)
    else:
        _gl.glLightfv(light, _gl.GL_QUADRATIC_ATTENUATION, _DEFAULT_QUADRATIC_ATTENUATION)


def is_light_enabled():
    """
    Check if lights are enabled.

    :return: Light is enabled
    :rtype: bool
    """
    return _OPENGL_CONFIGS[0]
