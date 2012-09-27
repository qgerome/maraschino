# -*- coding: utf-8 -*-
"""Ressources to use Maraschino on mobile devices"""

import jsonrpclib

from flask import render_template
from maraschino import app, logger

from maraschino.tools import *
from maraschino.noneditable import *
import maraschino


@app.route('/mobile/')
@requires_auth
def mobile_index():
    return render_template('mobile/index.html')


@app.route('/mobile/recent_episodes/')
@requires_auth
def recently_added_episodes():
    try:
        xbmc = jsonrpclib.Server(server_api_address())
        recently_added_episodes = xbmc.VideoLibrary.GetRecentlyAddedEpisodes(properties=['title', 'season', 'episode', 'showtitle', 'playcount', 'thumbnail', 'firstaired'])['episodes']

    except:
        logger.log('Could not retrieve recently added episodes', 'WARNING')

    return render_template('mobile/recent_episodes.html',
        recently_added_episodes=recently_added_episodes,
        webroot=maraschino.WEBROOT,
    )


@app.route('/mobile/recent_movies/')
@requires_auth
def recently_added_movies():
    try:
        xbmc = jsonrpclib.Server(server_api_address())
        recently_added_movies = xbmc.VideoLibrary.GetRecentlyAddedMovies(properties=['title', 'rating', 'year', 'thumbnail', 'tagline', 'playcount'])['movies']

    except:
        logger.log('Could not retrieve recently added movies', 'WARNING')

    return render_template('mobile/recent_movies.html',
        recently_added_movies=recently_added_movies,
        webroot=maraschino.WEBROOT,
    )


@app.route('/mobile/xbmc/')
@requires_auth
def xbmc():
    return render_template('mobile/xbmc.html',
        webroot=maraschino.WEBROOT,
    )


@app.route('/mobile/movie_library/')
@requires_auth
def movie_library():
    try:
        xbmc = jsonrpclib.Server(server_api_address())
        movies = xbmc.VideoLibrary.GetMovies(properties=['title', 'rating', 'year', 'thumbnail', 'tagline', 'playcount'])['movies']

    except:
        logger.log('Could not retrieve movie library', 'WARNING')

    return render_template('mobile/movie_library.html',
        movies=movies,
        webroot=maraschino.WEBROOT,
    )


@app.route('/mobile/tv_library/')
@requires_auth
def tv_library():
    try:
        xbmc = jsonrpclib.Server(server_api_address())
        TV = xbmc.VideoLibrary.GetTVShows(properties=['thumbnail'])['tvshows']

    except Exception as e:
        logger.log('Could not retrieve TV Shows: %s' % e, 'WARNING')

    return render_template('mobile/tv_library.html',
        TV=TV,
        webroot=maraschino.WEBROOT,
    )


@app.route('/mobile/tvshow/<int:id>/')
@requires_auth
def tvshow(id):
    try:
        xbmc = jsonrpclib.Server(server_api_address())
        show = xbmc.VideoLibrary.GetSeasons(tvshowid=id, properties=['tvshowid', 'season', 'showtitle', 'playcount'])['seasons']
        print show

    except Exception as e:
        logger.log('Could not retrieve TV Show [id: %i -  %s]' % (id, e), 'WARNING')

    return render_template('mobile/tvshow.html',
        show=show,
        webroot=maraschino.WEBROOT,
    )


@app.route('/mobile/tvshow/<int:id>/<int:season>/')
@requires_auth
def season(id, season):
    try:
        xbmc = jsonrpclib.Server(server_api_address())
        episodes = xbmc.VideoLibrary.GetEpisodes(tvshowid=id, season=season, sort={'method': 'episode'}, properties=['tvshowid', 'season', 'showtitle', 'playcount'])['episodes']

    except Exception as e:
        logger.log('Could not retrieve TV Show [id: %i, season: %i -  %s]' % (id, season, e), 'WARNING')

    return render_template('mobile/season.html',
        season=season,
        episodes=episodes,
        webroot=maraschino.WEBROOT,
    )
