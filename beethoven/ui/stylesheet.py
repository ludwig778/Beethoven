def get_stylesheet() -> str:
    return """
    * {
        padding: 0px;
        margin: 0px;
    }
    lol {
        border-radius: 0;
    }
    PushPullButton:checked {
        background-color: #66ff66;
    }

    FramedNotes {
        qproperty-alignment: AlignJustify;
        font-size: 18px;

        padding-top: 6px;
        padding-bottom: 6px;

        border: 1px solid lightGray;
        border-radius: 5px;
    }

    PushPullButton#start_button {
        background-color: #66ff66;
        height: 40px;
        width: 140px;
    }
    PushPullButton#start_button:checked {
        background-color: #aa4477;
    }

    Button#stop_button {
        background-color: red;
        height: 40px;
        width: 40px;
    }

    BaseTrainingWidget {
        background-color: blue;
    }
    ChordTrainingWidget {
        background-color: orange;
    }
    #lmao {
        background-color: orange;
        max-height: 33px;
    }
    PushPullButton#grid_item {
        height: 40px;
        width: 60px;
    }
    """
