

atsHistoryCmd = """
                    SELECT result, spread_outcome, money_outcome
                        FROM game_lines AS gl
                        INNER JOIN games AS g
                            ON gl.game_id = g.game_id AND gl.team_id = g.home_id
                        WHERE spread = ? AND game_type = 'season'
                    """


mLHistoryCmd = """
                    SELECT home.money, home.money_outcome, home.spread_outcome, home.spread, home.result,
                            away.money, away.money_outcome, away.spread_outcome, away.spread, away.result,
                            ov.ou, ov.outcome, ov.total
                        FROM game_lines AS home
                        INNER JOIN game_lines AS away
                            ON home.game_id = away.game_id AND home.team_id = away.opp_id
                        INNER JOIN games AS gm
                            ON home.game_id = gm.game_id AND home.team_id = gm.home_id
                        INNER JOIN over_unders AS ov
                            ON home.game_id = ov.game_id
                        WHERE game_type = 'season' {}
                        ORDER BY home.game_id DESC
                    """


totalHistoryCmd = """
                    SELECT total, ov.outcome
                        FROM over_unders AS ov
                        INNER JOIN games AS g
                            ON ov.game_id = g.game_id
                        WHERE ou = ? AND game_type = 'season'
                    """
