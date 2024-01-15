nbaNewPlayerCmd = """
            SELECT ps.player_id, first_name || ' ' || last_name, abrv,
                        COUNT(ps.game_id), AVG(starter)*100,
                        AVG(fga), AVG(fgm), SUM(fgm)/(SUM(fga)*1.0)*100, AVG(fta), AVG(ftm),
                        SUM(ftm)/(SUM(fta)*1.0)*100, AVG(tpa), AVG(tpm), SUM(tpm)/(SUM(tpa)*1.0)*100, AVG(pts),
                        AVG(oreb), AVG(reb), AVG(ast), AVG(stl), AVG(blk), AVG(trn),
                        AVG(fls), AVG(mins), AVG(plmn)
                FROM player_stats AS ps
                INNER JOIN players
                    ON ps.player_id = players.player_id
                INNER JOIN lineups
                    ON ps.game_id = lineups.game_id AND ps.player_id = lineups.player_id AND ps.team_id = lineups.team_id
                INNER JOIN position_types AS pt
                    ON players.pos_id = pt.pos_id
                WHERE ps.team_id = ? AND ps.{}
                GROUP BY ps.player_id
                HAVING AVG(mins) > 0
                ORDER BY AVG(pts) DESC
            """



nbaPlayerStatsCmd = """
                SELECT COUNT(ps.game_id), AVG(starter)*100,
                        AVG(fga), AVG(fgm), SUM(fgm)/(SUM(fga)*1.0)*100, AVG(fta), AVG(ftm),
                        SUM(ftm)/(SUM(fta)*1.0)*100, AVG(tpa), AVG(tpm), SUM(tpm)/(SUM(tpa)*1.0)*100, AVG(pts),
                        AVG(oreb), AVG(reb), AVG(ast), AVG(stl), AVG(blk), AVG(trn),
                        AVG(fls), AVG(mins), AVG(plmn)
                    FROM player_stats AS ps
                    INNER JOIN players
                        ON ps.player_id = players.player_id
                    INNER JOIN lineups
                        ON ps.game_id = lineups.game_id AND ps.player_id = lineups.player_id AND ps.team_id = lineups.team_id
                    WHERE ps.player_id = ? AND ps.{}
            """


ncaabPlayerStatsCmd = """
                SELECT ps.player_id, first_name || ' ' || last_name, abrv,
                            COUNT(ps.game_id), AVG(starter)*100,
                            AVG(fga), AVG(fgm), SUM(fgm)/(SUM(fga)*1.0)*100, AVG(fta), AVG(ftm),
                            SUM(ftm)/(SUM(fta)*1.0)*100, AVG(tpa), AVG(tpm), SUM(tpm)/(SUM(tpa)*1.0)*100, AVG(pts),
                            AVG(oreb), AVG(reb), AVG(ast), AVG(stl), AVG(blk), AVG(trn),
                            AVG(fls), AVG(mins)
                    FROM player_stats AS ps
                    INNER JOIN lineups
                        ON ps.game_id = lineups.game_id AND ps.player_id = lineups.player_id AND ps.team_id = lineups.team_id
                    INNER JOIN players
                        ON ps.player_id = players.player_id
                    INNER JOIN position_types AS pt
                        ON players.pos_id = pt.pos_id
                    WHERE ps.team_id = ? AND ps.{}
                    GROUP BY ps.player_id
                    HAVING AVG(mins) > 0
                    ORDER BY AVG(pts) DESC
            """
