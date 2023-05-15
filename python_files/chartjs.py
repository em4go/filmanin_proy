from pychartjs import BaseChart, ChartType, Color, Options


class SpiderChart(BaseChart):
    type = ChartType.Radar

    class data:
        data = [1, 1, 1, 1]
        label = "Numbers"
        backgroundColor = Color.RGBA(221, 83, 83, 0.5)
        # 221,83,83
        borderColor = Color.RGBA(221, 83, 83, 1)
        pointBackgroundColor = Color.White

    class options:
        # title = Options.Title(text="Wildlife Populations", fontSize=18)
        # _lables = Options.Legend_Labels(fontColor=Color.Blue, fullWidth=True)
        # legend = Options.Legend(position="Bottom", labels=_lables)
        scales = {"r": {"min": 0, "max": 10}}
        # Object-based
        animation = Options.General(duration=1000)

    class labels:
        names = ["name 1", "name 2", "name 3", "name 4"]


class ExampleChart(BaseChart):
    type = ChartType.Line

    class labels:
        pass

    class data:
        def __init__(self, data_list) -> None:
            self.data = data_list

        label = "Numbers"
        backgroundColor = Color.Green

    class options:
        pass

    class pluginOptions:
        pass
