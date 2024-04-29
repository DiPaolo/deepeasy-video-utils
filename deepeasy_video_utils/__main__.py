from deepeasy_video_utils.cli.cli import init_app, cli, deinit_app

# the very first call
init_app()

try:
    result = cli()
except Exception as ex:
    print(f'Unhandled Error: {ex}')
finally:
    deinit_app()
