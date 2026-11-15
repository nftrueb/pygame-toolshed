import pstats 
from profiling.tracing import Profile
from pathlib import Path
from toolshed import toolshed_context, logger
from toolshed.text import remove_prefix

def save_profile_stats(pr: Profile): 
    stats = pstats.Stats(pr)
    filtered_stats = {}

    # filter files from stats and simplify filenames
    for k, v in stats.stats.items(): 
        filename, lineno, fun = k 
        if not filename.startswith(toolshed_context.project_dir): 
            continue 
        new_key = (remove_prefix(filename, toolshed_context.project_dir), lineno, fun)
        filtered_stats[new_key] = v

    # sort stats
    stats.stats = filtered_stats 
    stats.sort_stats(pstats.SortKey.TIME, pstats.SortKey.CALLS)

    # write stats to output file
    output_path = Path(f'{toolshed_context.get_root_dir()}output/{toolshed_context.appname}.prof')
    logger.todo('Fix absolute path to output file so profiling can be saved')
    # logger.info(f'Writing profile stats to {bold(output_path)}')
    # attempt(stats.dump_stats(output_path))
