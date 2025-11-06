import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter


def extract_match_data(events_file_path):
    """
    JSON 데이터를 기반으로 경기 통계를 추출하는 함수

    매개변수:
    - events_file_path (str): JSON 파일 경로

    반환값:
    - dict: 팀별 경기 통계
    - list: 추출된 팀 이름 리스트
    - dict: 팀별 볼 점유율
    """
    with open(events_file_path, "r", encoding="utf-8") as f:
        events_data = json.load(f)

    teams = {}
    team_names = set()
    team_possession = {}
    total_duration = 0

    for event in events_data:
        team_name = event["team"]["name"]
        team_names.add(team_name)

        # 팀별 초기화
        if team_name not in teams:
            teams[team_name] = {
                "shots": 0,
                "on_target": 0,
                "fouls": 0,
                "yellow_cards": 0,
                "red_cards": 0,
                "offsides": 0,
                "corners": 0,
                "passes": 0,
                "pass_success": 0,
                "pass_success_rate": 0,
                "turnover_count": 0,
            }

        event_type = event["type"]["name"]
        # 볼 점유율 계산
        possession_team = event.get("possession_team", {}).get("name", None)
        duration = event.get("duration", 0)
        total_duration += duration
        team_possession[possession_team] = (
            team_possession.get(possession_team, 0) + duration
        )

        # 경기 통계 계산
        if event_type == "Shot":
            teams[team_name]["shots"] += 1
            outcome = event.get("shot", {}).get("outcome", {}).get("name", "")
            if outcome in [
                "Goal",
                "Saved",
                "Post",
                "Saved Off Target",
                "Saved to Post",
                "Blocked",
            ]:
                teams[team_name]["on_target"] += 1
        elif event_type == "Pass":
            teams[team_name]["passes"] += 1
            if "outcome" not in event.get("pass", {}):
                teams[team_name]["pass_success"] += 1
            elif event["pass"]["outcome"]["name"] == "Pass Offside":
                teams[team_name]["offsides"] += 1
            elif event["pass"].get("type", {}).get("name", "") == "Corner":
                teams[team_name]["corners"] += 1
        if event_type in ["Foul Committed", "Bad Behaviour"]:
            teams[team_name]["fouls"] += 1
            card_type1 = event.get("foul_committed", {}).get("card", {}).get("name", "")
            card_type2 = event.get("bad_behaviour", {}).get("card", {}).get("name", "")
            if card_type1 == "Yellow Card" or card_type2 == "Yellow Card":
                teams[team_name]["yellow_cards"] += 1
            elif card_type1 in ["Red Card", "Second Yellow"] or card_type2 in [
                "Red Card",
                "Second Yellow",
            ]:
                teams[team_name]["red_cards"] += 1

                # 볼 점유율 계산
    possession_percentages = {
        team: (time / total_duration) * 100 for team, time in team_possession.items()
    }

    # 패스 성공률 계산
    for team in teams:
        teams[team]["pass_success_rate"] = round(
            (teams[team]["pass_success"] / teams[team]["passes"]) * 100, 2
        )

    return teams, list(team_names), possession_percentages


def create_match_table(match_data, team_names, possession_percentages):
    """
    주어진 경기 데이터를 표로 출력하는 함수
    """
    columns = ["Category", team_names[0], team_names[1]]
    rows = [
        [
            "Shots",
            match_data[team_names[0]]["shots"],
            match_data[team_names[1]]["shots"],
        ],
        [
            "On Target",
            match_data[team_names[0]]["on_target"],
            match_data[team_names[1]]["on_target"],
        ],
        [
            "Possession",
            f"{possession_percentages[team_names[0]]:.2f}%",
            f"{possession_percentages[team_names[1]]:.2f}%",
        ],
        [
            "Passes",
            match_data[team_names[0]]["passes"],
            match_data[team_names[1]]["passes"],
        ],
        [
            "Pass Accuracy",
            f"{match_data[team_names[0]]['pass_success_rate']}%",
            f"{match_data[team_names[1]]['pass_success_rate']}%",
        ],
        [
            "Foul",
            match_data[team_names[0]]["fouls"],
            match_data[team_names[1]]["fouls"],
        ],
        [
            "Yellow Card",
            match_data[team_names[0]]["yellow_cards"],
            match_data[team_names[1]]["yellow_cards"],
        ],
        [
            "Red Card",
            match_data[team_names[0]]["red_cards"],
            match_data[team_names[1]]["red_cards"],
        ],
        [
            "Offside",
            match_data[team_names[0]]["offsides"],
            match_data[team_names[1]]["offsides"],
        ],
        [
            "Corners",
            match_data[team_names[0]]["corners"],
            match_data[team_names[1]]["corners"],
        ],
    ]

    df = pd.DataFrame(rows, columns=columns)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(
        cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    table.scale(1, 1.5)

    plt.title("Match Statistics", fontsize=16, fontweight="bold")
    plt.show()


def extract_record_data(events_file_path):
    """
    JSON 데이터를 기반으로 선수별 데이터를 추출하는 함수

    매개변수:
    - events_file_path (str): JSON 파일 경로

    반환값:
    - None: 분야별 Most Player를 표로 출력

    """
    with open(events_file_path, "r", encoding="utf-8") as f:
        events_data = json.load(f)

    record_count = Counter()

    # 이벤트 데이터를 순회하면서 'Shot', 'Dribble', 'Pass' 카운트
    for event in events_data:
        event_type = event.get("type", {}).get("name", None)
        player_name = event.get("player", {}).get("name", None)

        if event_type == "Shot":
            record_count[(player_name, "Shot")] += 1
        elif (
            event_type == "Dribble"
            and event.get("dribble", {}).get("outcome", {}).get("name", None)
            == "Complete"
        ):
            record_count[(player_name, "Dribble")] += 1
        elif event_type == "Pass" and "outcome" not in event.get(
            "pass", {}
        ):  # pass.outcome이 없을 때 -> 성공한 패스
            record_count[(player_name, "Pass")] += 1

    player_record = {}
    for (player, action), count in record_count.items():
        if player not in player_record:
            player_record[player] = {"Dribble": 0, "Shot": 0, "Pass": 0}
        player_record[player][action] = count

    player_name = []
    dribble_list = []
    shot_list = []
    pass_list = []

    for player, actions in player_record.items():
        player_name.append(player)
        dribble_list.append(actions["Dribble"])
        shot_list.append(actions["Shot"])
        pass_list.append(actions["Pass"])

    # DataFrame 생성
    my_df_dribble = pd.DataFrame(
        {
            "Player": player_name,
            "Dribble": dribble_list,
        }
    )
    max_dribbler = my_df_dribble.loc[my_df_dribble["Dribble"].idxmax()]

    my_df_shot = pd.DataFrame({"Player": player_name, "Shot": shot_list})
    max_shooter = my_df_shot.loc[my_df_shot["Shot"].idxmax()]

    my_df_pass = pd.DataFrame({"Player": player_name, "Pass": pass_list})
    max_passer = my_df_pass.loc[my_df_pass["Pass"].idxmax()]

    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(8, 6))

    # 드리블 통계
    ax[0].axis("tight")
    ax[0].axis("off")
    table_data = [
        ["Player", "Dribble"],
        [max_dribbler["Player"], max_dribbler["Dribble"]],
    ]
    table = ax[0].table(cellText=table_data, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=1)
    table.scale(1, 1.5)
    ax[0].set_title("Most Dribbler", fontsize=16, fontweight="bold")

    # 슛 통계
    ax[1].axis("tight")
    ax[1].axis("off")
    table_data = [["Player", "Shot"], [max_shooter["Player"], max_shooter["Shot"]]]
    table = ax[1].table(cellText=table_data, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=1)
    table.scale(1, 1.5)
    ax[1].set_title("Most Shooter", fontsize=16, fontweight="bold")

    # 패스 통계
    ax[2].axis("tight")
    ax[2].axis("off")
    table_data = [["Player", "Pass"], [max_passer["Player"], max_passer["Pass"]]]
    table = ax[2].table(cellText=table_data, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=1)
    table.scale(1, 1.5)
    ax[2].set_title("Most Passer", fontsize=16, fontweight="bold")

    plt.show()


if __name__ == "__main__":
    # 파일 경로
    events_file_path = "/Users/kyuhyeon/Documents/data/events/3773457.json"

    # 데이터 추출
    teams, team_names, possession_percentages = extract_match_data(events_file_path)

    # 표 생성 및 출력
    create_match_table(teams, team_names, possession_percentages)

    # most player
    extract_record_data(events_file_path)
