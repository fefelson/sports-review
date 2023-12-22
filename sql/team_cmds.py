gamePoolCmd = """
                SELECT gm.game_id,
                        game_time,
                        team.opp_id,
                        CAST(((team.fga)+(team.trn)+(.44*(team.fta))-(team.oreb)) * 48.0 / (minutes) +
                        ((opp.fga)+(opp.trn)+(.44*(opp.fta))-(opp.oreb)) * 48.0 / (minutes) AS int) AS poss,
                        team.pts,
                        opp.pts,
                        CASE WHEN gl.team_id == home_id THEN 1 ELSE 0 END AS is_home,
                        CASE WHEN gl.team_id == winner_id THEN 1 ELSE 0 END AS is_winner,
                        result,
                        money,
                        spread,
                        ou,
                        spread_outcome AS is_cover,
                        ov.outcome AS is_over
                    FROM team_stats AS team
                    INNER JOIN team_stats AS opp
                        ON team.game_id = opp.game_id AND team.team_id = opp.opp_id
                    INNER JOIN games AS gm
                        ON team.game_id = gm.game_id AND (team.team_id = gm.away_id OR team.team_id = gm.home_id)
                    INNER JOIN game_lines AS gl
                        ON team.game_id = gl.game_id AND team.team_id = gl.team_id
                    INNER JOIN over_unders AS ov
                        ON gm.game_id = ov.game_id
                    WHERE season = ? AND gl.team_id = ?
                    ORDER BY gm.game_id DESC
                """

teamOddsCmd = """
                SELECT ROUND(AVG(team.spread), 2),
                        ROUND(AVG(team.result), 2),
                        ROUND(AVG(team.money), 2),
                        ROUND((SUM((CASE WHEN team.spread_outcome == 1 THEN (10000/(-110*-1.0))+100
                                        WHEN team.spread_outcome == 0 THEN 100
                                        ELSE 0 END))-(COUNT(team.spread_outcome)*100))/COUNT(team.spread_outcome), 2) AS spread_roi,
                        ROUND((SUM((CASE WHEN team.money_outcome == 1 AND team.money > 0 THEN 100+team.money
                                WHEN team.money_outcome == 1 AND team.money < 0 THEN (10000/(team.money*-1.0))+100
                                ELSE 0 END))-(COUNT(team.money)*100))/COUNT(team.money), 2) AS money_roi,

                        ROUND((SUM((CASE WHEN opp.spread_outcome == 1 THEN (10000/(-110*-1.0))+100
                                        WHEN opp.spread_outcome == 0 THEN 100
                                        ELSE 0 END))-(COUNT(opp.spread_outcome)*100))/COUNT(opp.spread_outcome), 2) AS spread_roi,
                        ROUND((SUM((CASE WHEN opp.money_outcome == 1 AND opp.money > 0 THEN 100+opp.money
                                WHEN opp.money_outcome == 1 AND opp.money < 0 THEN (10000/(opp.money*-1.0))+100
                                ELSE 0 END))-(COUNT(opp.money)*100))/COUNT(opp.money), 2) AS opp_money_roi,

                        ROUND(AVG(ou), 2),
                        ROUND(AVG(total), 2),
                        ROUND((SUM((CASE WHEN outcome == 1 AND over_line > 0 THEN 100+over_line
                                WHEN outcome == 1 AND over_line < 0 THEN (10000/(over_line*-1.0))+100
                                WHEN outcome == 0 THEN 100
                                ELSE 0 END))-(COUNT(outcome)*100))/COUNT(outcome), 2),
                        ROUND( (SUM(CASE WHEN outcome == -1 AND under_line > 0 THEN 100+under_line
                                WHEN outcome == -1 AND under_line < 0 THEN (10000/(under_line*-1.0))+100
                                WHEN outcome == 0 THEN 100
                                ELSE 0 END)-(COUNT(outcome)*100))/COUNT(outcome), 2)
                    FROM game_lines AS team
                    INNER JOIN game_lines AS opp
                        ON team.game_id = opp.game_id AND team.team_id = opp.opp_id
                    INNER JOIN over_unders AS ov
                        ON team.game_id = ov.game_id
                    WHERE team.team_id = ? AND team.{}
                """


teamRecordsCmd = """
                SELECT IFNULL(SUM(CASE WHEN money_outcome == 1 THEN 1 ELSE 0 END), 0) AS game_win,
                        IFNULL(SUM(CASE WHEN money_outcome == -1 THEN 1 ELSE 0 END), 0) AS game_loss,
                        IFNULL(SUM(CASE WHEN money_outcome == 0 THEN 1 ELSE 0 END), 0) AS game_push,
                        ROUND(IFNULL(SUM(CASE WHEN money_outcome == 1 THEN 1 ELSE 0 END), 0) *1.0 / IFNULL(COUNT(gl.game_id), 1)*100, 2)  AS win_pct,

                        IFNULL(SUM(CASE WHEN spread_outcome == 1 THEN 1 ELSE 0 END), 0) AS spread_win,
                        IFNULL(SUM(CASE WHEN spread_outcome == -1 THEN 1 ELSE 0 END), 0) AS spread_loss,
                        IFNULL(SUM(CASE WHEN spread_outcome == 0 THEN 1 ELSE 0 END), 0) AS spread_push,
                        ROUND(IFNULL(SUM(CASE WHEN spread_outcome == 1 THEN 1 ELSE 0 END), 0) *1.0 / IFNULL(COUNT(spread_outcome), 1)*100, 2) AS spread_pct,

                        IFNULL(SUM(CASE WHEN outcome == 1 THEN 1 ELSE 0 END), 0) AS total_over,
                        IFNULL(SUM(CASE WHEN outcome == -1 THEN 1 ELSE 0 END), 0) AS total_under,
                        IFNULL(SUM(CASE WHEN outcome == 0 THEN 1 ELSE 0 END), 0) AS total_push,
                        ROUND(IFNULL(SUM(CASE WHEN outcome == 1 THEN 1 ELSE 0 END), 0) *1.0 / IFNULL(COUNT(outcome), 1)*100, 2) AS over_pct
                    FROM game_lines AS gl
                    INNER JOIN over_unders AS ov
                        ON gl.game_id = ov.game_id
                    WHERE gl.team_id = ? AND gl.{}
                """

teamStatsCmd = """
                SELECT COUNT(team.game_id) AS gp,
                        ROUND(SUM(team.pts) / (SUM(team.fga)+SUM(team.trn)+(.44*SUM(team.fta))-SUM(team.oreb)) * 100, 2) AS off_eff,
                        ROUND(SUM(opp.pts) / (SUM(opp.fga)+SUM(opp.trn)+(.44*SUM(opp.fta))-SUM(opp.oreb)) * 100, 2) AS def_eff,
                        ROUND((SUM(team.pts) / (SUM(team.fga)+SUM(team.trn)+(.44*SUM(team.fta))-SUM(team.oreb)) * 100)
                            - (SUM(opp.pts) / (SUM(opp.fga)+SUM(opp.trn)+(.44*SUM(opp.fta))-SUM(opp.oreb)) * 100), 2) AS score,
                        CAST(((SUM(team.fga)+SUM(team.trn)+(.44*SUM(team.fta))-SUM(team.oreb)) * 48.0 / SUM(minutes))
                            + ((SUM(opp.fga)+SUM(opp.trn)+(.44*SUM(opp.fta))-SUM(opp.oreb)) * 48.0 / SUM(minutes)) AS int) AS game_poss,
                        CAST((SUM(team.fga)+SUM(team.trn)+(.44*SUM(team.fta))-SUM(team.oreb)) * 48.0 / SUM(minutes) AS int) AS team_poss,
                        ROUND(SUM(team.pts) / (SUM(minutes) /48.0 ), 2) AS team_pts,
                        ROUND(SUM(team.fga) / (SUM(minutes) /48.0 ), 2) AS team_fga,
                        ROUND(SUM(team.fgm) / (SUM(minutes) /48.0 ), 2) AS team_fgm,
                        ROUND((SUM(team.fgm)*1.0)/SUM(team.fga)*100.0, 2) AS team_fgpct,
                        ROUND(SUM(team.fta) / (SUM(minutes) /48.0 ), 2) AS team_fta,
                        ROUND(SUM(team.ftm) / (SUM(minutes) /48.0 ), 2) AS team_ftm,
                        ROUND((SUM(team.ftm)*1.0)/SUM(team.fta)*100.0, 2) AS team_ftpct,
                        ROUND(SUM(team.tpa) / (SUM(minutes) /48.0 ), 2) AS team_tpa,
                        ROUND(SUM(team.tpm) / (SUM(minutes) /48.0 ), 2) AS team_tpm,
                        ROUND((SUM(team.tpm)*1.0)/SUM(team.tpa)*100.0, 2) AS team_tppct,
                        ROUND(SUM(team.trn)/(SUM(team.fga) + (0.44 * SUM(team.fta)) - SUM(team.oreb) + SUM(team.trn))*100.0, 2) AS team_tov,
                        ROUND(AVG(team.oreb) / (AVG(team.oreb) + AVG(opp.dreb))*100.0, 2) AS team_oreb_pct,
                        ROUND(AVG(team.dreb) / (AVG(team.dreb) + AVG(opp.oreb))*100.0, 2) AS team_dreb_pct,

                        CAST((SUM(opp.fga)+SUM(opp.trn)+(.44*SUM(opp.fta))-SUM(opp.oreb)) * 48.0 / SUM(minutes) AS int)  AS opp_poss,
                        ROUND(SUM(opp.pts) / (SUM(minutes) /48.0 ), 2) AS opp_pts,
                        ROUND(SUM(opp.fga) / (SUM(minutes) /48.0 ), 2) AS opp_fga,
                        ROUND(SUM(opp.fgm) / (SUM(minutes) /48.0 ), 2) AS opp_fgm,
                        ROUND((SUM(opp.fgm)*1.0)/SUM(opp.fga)*100.0 , 2)AS opp_fgpct,
                        ROUND(SUM(opp.fta) / (SUM(minutes) /48.0 ), 2) AS opp_fta,
                        ROUND(SUM(opp.ftm) / (SUM(minutes) /48.0 ), 2) AS opp_ftm,
                        ROUND((SUM(opp.ftm)*1.0)/SUM(opp.fta)*100.0, 2) AS opp_ftpct,
                        ROUND(SUM(opp.tpa) / (SUM(minutes) /48.0 ), 2) AS opp_tpa,
                        ROUND(SUM(opp.tpm) / (SUM(minutes) /48.0 ), 2) AS opp_tpm,
                        ROUND((SUM(opp.tpm)*1.0)/SUM(opp.tpa)*100.0, 2) AS opp_tppct,
                        ROUND(SUM(opp.trn)/(SUM(opp.fga) + (0.44 * SUM(opp.fta)) - SUM(opp.oreb) + SUM(opp.trn))*100.0, 2) AS opp_tov,
                        ROUND(AVG(opp.oreb) / (AVG(opp.oreb) + AVG(team.dreb))*100.0, 2) AS opp_oreb_pct,
                        ROUND(AVG(opp.dreb) / (AVG(opp.dreb) + AVG(team.oreb))*100.0, 2) AS opp_dreb_pct

                    FROM team_stats AS team
                    INNER JOIN games AS gm
                        ON team.game_id = gm.game_id AND (team.team_id = gm.home_id OR team.team_id = gm.away_id)
                    INNER JOIN team_stats AS opp
                        ON team.game_id = opp.game_id AND team.team_id = opp.opp_id
                    WHERE team.team_id = ? AND gm.{}
                """
