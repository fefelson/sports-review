



mLHistoryCmd = """
                    SELECT team.money, team.money_outcome, team.spread_outcome, team.spread, team.result,
                            opp.money, opp.money_outcome, opp.spread_outcome, opp.spread, opp.result
                        FROM game_lines AS team
                        INNER JOIN game_lines AS opp
                            ON team.game_id = opp.game_id AND team.team_id = opp.opp_id
                        INNER JOIN games AS gm
                            ON team.game_id = gm.game_id AND team.team_id = gm.home_id
                        WHERE game_type = 'season' AND team.money = ? AND opp.money = ?
                        ORDER BY team.game_id DESC
                    """
