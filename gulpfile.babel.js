'use strict';

import gulp from 'gulp';
import concat from 'gulp-concat';
import cssjoin from 'gulp-cssjoin';
import eslint from 'gulp-eslint';
import rename from 'gulp-rename';
import sass from 'gulp-sass';
import sequence from 'gulp-sequence';
import size from 'gulp-size';
import sourcemaps from 'gulp-sourcemaps';
import tslint from 'gulp-tslint';
import named from 'vinyl-named';

import webpackStream from 'webpack-stream';
import webpackConfigFactory from './webpack.factory';

const gulpConfig = {
    css: {
        src: 'src/stylesheets/',
        entries:[
            'src/stylesheets/main.scss',
            'src/stylesheets/admin.scss'
        ],
        dest: 'public/stylesheets/'
    },
    fonts: {
        src: [
            'node_modules/bootstrap/fonts/**/*',
            'node_modules/font-awesome/fonts/**/*'
        ],
        dest: 'public/fonts/'
    },
    js: {
        vendors: [
            'node_modules/jquery/dist/jquery.min.js',
            'node_modules/bootstrap/dist/js/bootstrap.min.js'
        ],
        src: 'angular/',
        entries: [
            'angular/main.ts'
        ],
        dest: 'public/javascripts/'
    }
};

gulp.task('default', ['build']);

gulp.task('dev', ['dev:server', 'dev:webpack']);
gulp.task('build', sequence('build:assets', 'build:lint', 'build:webpack'));
gulp.task('deploy', ['deploy:hostpoint']);

/*
 * Dev
 */

gulp.task('dev:webpack', () => {
    let wpConfig = webpackConfigFactory(gulpConfig.js.src, false, {
        watch: true
    });

    let wpStream = webpackStream(wpConfig);
    // bind the error in order not to stop the watch when an error occurs
    wpStream.on('error', () => {});

    return gulp.src(gulpConfig.js.entries)
        .pipe(named())
        .pipe(wpStream)
        .pipe(gulp.dest(gulpConfig.js.dest));
});

/*
 * Build
 */

function printBuilt() {
    return size({
        showFiles: true,
        showTotal: false
    });
}

gulp.task('build:assets', ['build:assets:css', 'build:assets:fonts', 'build:assets:vendors']);

// Stylesheets

gulp.task('build:assets:css', () => {
    return gulp.src(gulpConfig.css.entries)
        .pipe(sourcemaps.init())
        .pipe(cssjoin())
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(rename({
            extname: '.min.css'
        }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(gulpConfig.css.dest))
        .pipe(printBuilt());
});

// Fonts

gulp.task('build:assets:fonts', () => {
    return gulp.src(gulpConfig.fonts.src)
        .pipe(gulp.dest(gulpConfig.fonts.dest))
        .pipe(printBuilt());
});

// Vendors

gulp.task('build:assets:vendors', () => {
    return gulp.src(gulpConfig.js.vendors)
        .pipe(concat('vendors.js'))
        .pipe(gulp.dest(gulpConfig.js.dest))
        .pipe(printBuilt());
});

// Lint

gulp.task('build:lint', sequence('build:lint:es', 'build:lint:ts'));

gulp.task('build:lint:es', () => {
    return gulp.src([gulpConfig.js.src + '**/*.js', '!node_modules/**'])
        .pipe(eslint('.eslintrc'))
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});

gulp.task('build:lint:ts', () => {
    return gulp.src([gulpConfig.js.src + '**/*.ts', '!node_modules/**'])
        .pipe(tslint({
            formatter: "verbose"
        }))
        .pipe(tslint.report())
});

// Webpack

gulp.task('build:webpack', () => {
    return gulp.src(gulpConfig.js.entries)
        .pipe(named())
        .pipe(webpackStream(webpackConfigFactory(gulpConfig.js.src, true)))
        .pipe(gulp.dest(gulpConfig.js.dest));
});