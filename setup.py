#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-worldmovie-central.jarbasai=skill_worldmovie_central:WorldMovieCentralSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-worldmovie-central',
    version='0.0.1',
    description='ovos classic worldmovie worldmovie skill plugin',
    url='https://github.com/JarbasSkills/skill-worldmovie-central',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_worldmovie_central": ""},
    package_data={'skill_worldmovie_central': ['locale/*', 'ui/*']},
    packages=['skill_worldmovie_central'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
