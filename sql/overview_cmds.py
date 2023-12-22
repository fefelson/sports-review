
overviewCmd = """
                SELECT abrv, COUNT(gm.game_id),
                ROUND( ((SUM(CASE WHEN team.team_id = winner_id THEN 1 ELSE 0 END)*1.0) / IFNULL(COUNT(gm.game_id), 1))*100 , 1) AS win_pct,
                CAST(AVG(team.money) AS int) AS team_money,

                ROUND((SUM((CASE WHEN team.money_outcome == 1 AND team.money > 0 THEN 100+team.money
                        WHEN team.money_outcome == 1 AND team.money < 0 THEN (10000/(team.money*-1.0))+100
                        ELSE 0 END))-(COUNT(team.game_id)*100))/COUNT(team.game_id), 2) AS money_roi,

                CAST(AVG(opp.money) AS int) AS opp_money,

                ROUND((SUM((CASE WHEN opp.money_outcome == 1 AND opp.money > 0 THEN 100+opp.money
                        WHEN opp.money_outcome == 1 AND opp.money < 0 THEN (10000/(opp.money*-1.0))+100
                        ELSE 0 END))-(COUNT(team.game_id)*100))/COUNT(team.game_id), 2) AS opp_money_roi,

                ROUND(AVG(team.spread), 1), ROUND(AVG(team.result), 1),

                ROUND( ((SUM(CASE WHEN team.spread_outcome = 1 THEN 1 ELSE 0 END)*1.0) / IFNULL(COUNT(gm.game_id), 1))*100 , 1) AS cover_pct,

                ROUND((SUM((CASE WHEN team.spread_outcome == 1 THEN (10000/(-110*-1.0))+100
                                WHEN team.spread_outcome == 0 THEN 100
                                ELSE 0 END))-(COUNT(team.game_id)*100))/COUNT(team.game_id), 2) AS spread_roi,

                ROUND(AVG(ov.ou), 1), ROUND(AVG(ov.total), 1),

                ROUND(IFNULL(SUM(CASE WHEN ov.outcome == 1 THEN 1 ELSE 0 END), 0) *1.0 / IFNULL(COUNT(ov.game_id), 1)*100, 2) AS over_pct,

                ROUND((SUM((CASE WHEN outcome == 1 AND over_line > 0 THEN 100+over_line
                        WHEN outcome == 1 AND over_line < 0 THEN (10000/(over_line*-1.0))+100
                        WHEN outcome == 0 THEN 100
                        ELSE 0 END))-(COUNT(ov.game_id)*100))/COUNT(ov.game_id), 2) AS over_roi,

                ROUND( (SUM(CASE WHEN outcome == -1 AND under_line > 0 THEN 100+under_line
                        WHEN outcome == -1 AND under_line < 0 THEN (10000/(under_line*-1.0))+100
                        WHEN outcome == 0 THEN 100
                        ELSE 0 END)-(COUNT(ov.game_id)*100))/COUNT(ov.game_id), 2) AS under_roi,

                team.team_id

            FROM game_lines AS team
            INNER JOIN game_lines AS opp
                ON team.game_id = opp.game_id AND team.team_id = opp.opp_id
            INNER JOIN games AS gm
                ON team.game_id = gm.game_id AND (team.team_id = gm.home_id OR team.team_id = gm.away_id)
            INNER JOIN teams AS team_info
                ON team.team_id = team_info.team_id
            INNER JOIN over_unders AS ov
                ON team.game_id = ov.game_id
            WHERE season = ? AND team.opp_id != -1 AND ou > 0
            GROUP BY team.team_id
            ORDER BY team.team_id DESC
                """


teamReportCmd = """
                SELECT ROUND(((SUM(CASE WHEN gl.team_id = winner_id THEN 1 ELSE 0 END)*1.0) / IFNULL(COUNT(gm.game_id), 2))*100 , 1) AS win_pct,
                        ROUND(((SUM(CASE WHEN spread_outcome = 1 THEN 1 ELSE 0 END)*1.0) / IFNULL(COUNT(spread), 1))*100 , 2) AS cover_pct,
                        ROUND(IFNULL(SUM(CASE WHEN ov.outcome == 1 THEN 1 ELSE 0 END), 0) *1.0 / IFNULL(COUNT(ou), 1)*100, 2) AS over_pct,
                        ROUND(IFNULL(SUM(CASE WHEN ov.outcome == -1 THEN 1 ELSE 0 END), 0) *1.0 / IFNULL(COUNT(ou), 1)*100, 2) AS under_pct,

                        ROUND((SUM((CASE WHEN money_outcome == 1 AND money > 0 THEN 100+money
                                WHEN money_outcome == 1 AND money < 0 THEN (10000/(money*-1.0))+100
                                ELSE 0 END))-(COUNT(money)*100))/COUNT(money), 2) AS money_roi,

                        ROUND((SUM((CASE WHEN spread_outcome == 1 THEN (10000/(-110*-1.0))+100
                                WHEN spread_outcome == 0 THEN 100
                                ELSE 0 END))-(COUNT(spread)*100))/COUNT(spread), 2) AS ats_roi,

                        ROUND((SUM((CASE WHEN outcome == 1 THEN (10000/(-110*-1.0))+100
                                WHEN outcome == 0 THEN 100
                                ELSE 0 END))-(COUNT(ou)*100))/COUNT(ou), 2) AS over_roi,

                        ROUND((SUM((CASE WHEN outcome == -1 THEN (10000/(-110*-1.0))+100
                                WHEN outcome == 0 THEN 100
                                ELSE 0 END))-(COUNT(ou)*100))/COUNT(ou), 2) AS under_roi,

                        ROUND(SUM(team.pts) / (SUM(team.fga)+SUM(team.trn)+(.44*SUM(team.fta))-SUM(team.oreb)) * 100, 2) AS off_eff,

                        ROUND(SUM(opp.pts) / (SUM(opp.fga)+SUM(opp.trn)+(.44*SUM(opp.fta))-SUM(opp.oreb)) * 100, 2) AS def_eff,

                        ROUND((SUM(team.pts) / (SUM(team.fga)+SUM(team.trn)+(.44*SUM(team.fta))-SUM(team.oreb)) * 100)
                            - (SUM(opp.pts) / (SUM(opp.fga)+SUM(opp.trn)+(.44*SUM(opp.fta))-SUM(opp.oreb)) * 100), 2) AS score,

                        ROUND(((SUM(team.fga)+SUM(team.trn)+(.44*SUM(team.fta))-SUM(team.oreb)) * 48.0 / SUM(minutes))
                            + ((SUM(opp.fga)+SUM(opp.trn)+(.44*SUM(opp.fta))-SUM(opp.oreb)) * 48.0 / SUM(minutes)), 2) AS game_poss,

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
                        ROUND(AVG(team.dreb) / (AVG(team.dreb) + AVG(opp.oreb))*100.0, 2) AS team_dreb_pct

                    FROM team_stats AS team
                    INNER JOIN team_stats AS opp
                        ON team.game_id = opp.game_id AND team.team_id = opp.opp_id
                    INNER JOIN game_lines AS gl
                        ON team.game_id = gl.game_id AND team.team_id = gl.team_id
                    INNER JOIN over_unders AS ov
                        ON team.game_id = ov.game_id
                    INNER JOIN games AS gm
                        ON team.game_id = gm.game_id AND (team.team_id = gm.away_id OR team.team_id = gm.home_id)

                    WHERE season = ?
                    GROUP BY team.team_id
                """
