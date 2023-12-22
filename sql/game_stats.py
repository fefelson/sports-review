gameStatsCmd = """
                    SELECT team_name.last_name,
                            CAST(((team.fga)+(team.trn)+(.44*(team.fta))-(team.oreb)) * 48.0 / (minutes) AS int) AS team_poss,
                            (team.pts) AS team_pts,
                            (team.fga) AS team_fga,
                            (team.fgm) AS team_fgm,
                            ((team.fgm)*1.0)/(team.fga)*100.0 AS team_fgpct,
                            (team.fta) AS team_fta,
                            (team.ftm)  AS team_ftm,
                            ((team.ftm)*1.0)/(team.fta)*100.0 AS team_ftpct,
                            (team.tpa) AS team_tpa,
                            (team.tpm) AS team_tpm,
                            (SUM(team.tpm)*1.0)/SUM(team.tpa)*100.0 AS team_tppct,
                            (team.trn*1.0)/((team.fga) + (0.44 * (team.fta)) - (team.oreb) + (team.trn))*100.0 AS team_tov,
                            (team.oreb *1.0) / ((team.oreb) + (opp.dreb))*100.0 AS team_oreb_pct,
                            (team.dreb *1.0) / ((team.dreb) + (opp.oreb))*100.0 AS team_dreb_pct,

                            opp_name.last_name,
                            ((opp.fga)+(opp.trn)+(.44*(opp.fta))-(opp.oreb)) * 48.0 / SUM(minutes)  AS opp_poss,
                            (opp.pts) AS opp_pts,
                            (opp.fga) AS opp_fga,
                            (opp.fgm) AS opp_fgm,
                            ((opp.fgm)*1.0)/(opp.fga)*100.0 AS opp_fgpct,
                            (opp.fta) AS opp_fta,
                            (opp.ftm) AS opp_ftm,
                            ((opp.ftm)*1.0)/(opp.fta)*100.0 AS opp_ftpct,
                            (opp.tpa) AS opp_tpa,
                            (opp.tpm) AS opp_tpm,
                            ((opp.tpm)*1.0)/(opp.tpa)*100.0 AS opp_tppct,
                            (opp.trn*1.0)/((opp.fga) + (0.44 * (opp.fta)) - (opp.oreb) + (opp.trn))*100.0 AS opp_tov,
                            (opp.oreb *1.0) / ((opp.oreb) + (team.dreb))*100 AS opp_oreb_pct,
                            (opp.dreb *1.0) / ((opp.dreb) + (team.oreb))*100 AS opp_dreb_pct

                        FROM team_stats AS team
                        INNER JOIN teams AS team_name
                            ON team.team_id = team_name.team_id
                        INNER JOIN games AS gm
                            ON team.game_id = gm.game_id AND (team.team_id = gm.home_id OR team.team_id = gm.away_id)
                        INNER JOIN team_stats AS opp
                            ON team.game_id = opp.game_id AND team.team_id = opp.opp_id
                        INNER JOIN teams AS opp_name
                            ON opp.team_id = opp_name.team_id
                        WHERE team.game_id = ? AND team.opp_id = ?
                    """
