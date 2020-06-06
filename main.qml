import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.11
import QtQuick3D 1.15
import QtQuick.Controls 1.4 as QQC1
import QtQuick.Controls 2.15 as QQC2
import QtQuick.Controls.Styles 1.4

QQC2.ApplicationWindow {
    id: window
    title: qsTr("Hello World")
    width: 800
    height: 480
    color: "#000000"
    visible: true

    Rectangle {
        id: rectangle1
        width: 800
        height: 480
        color: "#000000"

        Text {
            id: txtGear
            objectName: "txtGear"
            x: 0
            y: 80
            width: 150
            height: 200
            color: "#ffffff"
            text: car.gear
            font.weight: Font.DemiBold
            anchors.horizontalCenterOffset: 0
            font.family: "Arial"
            visible: true
            anchors.horizontalCenter: parent.horizontalCenter
            topPadding: 0
            font.kerning: true
            font.capitalization: Font.AllUppercase
            enabled: true
            lineHeight: 1
            fontSizeMode: Text.FixedSize
            renderType: Text.QtRendering
            textFormat: Text.AutoText
            maximumLineCount: 0
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            clip: false
            font.preferShaping: false
            font.bold: true
            font.pixelSize: 250

            QQC2.Label {
                id: txtCarBehind1
                objectName: "txtDiffPreviousLap"
                x: 2
                width: 150
                height: 34
                color: "#28f054"
                text: qsTr("-100.344")
                verticalAlignment: Text.AlignVCenter
                font.capitalization: Font.AllUppercase
                font.weight: Font.DemiBold
                font.family: "Arial"
                anchors.top: parent.bottom
                anchors.topMargin: 10
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.rightMargin: 10
                font.pointSize: 30
                font.bold: true
            }
        }

        Rectangle {
            id: info1
            x: 0
            y: 100
            width: 250
            height: 142
            color: "#000000"
            anchors.left: parent.left
            anchors.leftMargin: 20
            border.width: 2
            border.color: "gray"

            QQC2.Label {
                id: txtSpeed
                objectName: "txtSpeed"
                x: 0
                y: 0
                width: 250
                height: 48
                color: "#ffffff"
                text: car.speed + " KPM"
                font.styleName: "Bold"
                verticalAlignment: Text.AlignVCenter
                fontSizeMode: Text.HorizontalFit
                horizontalAlignment: Text.AlignHCenter
                font.bold: true
                font.pixelSize: 36
                background: Rectangle {
                    color: "gray"
                }
            }

            QQC2.Label {
                id: txtLap
                objectName: "txtLap"
                y: 57
                width: 74
                height: 36
                color: "#ffffff"
                text: "L" + lap.currentLapNum
                anchors.left: parent.left
                anchors.leftMargin: 10
                font.pointSize: 30
                font.bold: true
            }


            QQC2.Label {
                id: txtPosition
                objectName: "txtPosition"
                x: 176
                y: 57
                width: 66
                height: 36
                color: "#ffffff"
                text: "P" + lap.position
                horizontalAlignment: Text.AlignRight
                anchors.right: parent.right
                anchors.rightMargin: 10
                font.pointSize: 30
                font.bold: true
            }

            QQC2.Label {
                id: txtCarAhead
                objectName: "txtCarAhead"
                x: 8
                y: 99
                width: 76
                height: 36
                color: "#ffffff"
                text: qsTr("3.4")
                anchors.leftMargin: 10
                font.pointSize: 30
                font.bold: true
            }

            QQC2.Label {
                id: txtCarBehind
                objectName: "txtCarBehind"
                x: 96
                y: 99
                color: "#28f054"
                text: qsTr("(+300.34)")
                anchors.rightMargin: 10
                horizontalAlignment: Text.AlignRight
                font.pointSize: 30
                font.bold: true
            }
        }

        Rectangle {
            id: info2
            x: 0
            y: 100
            width: 250
            height: 142
            color: "#000000"
            anchors.right: parent.right
            anchors.rightMargin: 20
            border.width: 2
            QQC2.Label {
                id: txtLapTime
                objectName: "txtLapTime"
                x: 0
                y: 0
                width: 250
                height: 48
                color: "#ffffff"
                text: lap.currentLapTime
                background: Rectangle {
                    color: "#808080"
                }
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                fontSizeMode: Text.HorizontalFit
                font.pixelSize: 36
                font.styleName: "Bold"
                font.bold: true
            }

            QQC2.Label {
                id: txtTireLeft1
                objectName: "txtTireLeft1"
                y: 57
                width: 97
                height: 36
                color: "#ffffff"
                text: car.tyresSurfaceTemperature[0] + "°C"
                anchors.left: parent.left
                anchors.leftMargin: 10
                font.pointSize: 30
                font.bold: true
            }

            QQC2.Label {
                id: txtTireLeft2
                objectName: "txtTireLeft2"
                y: 99
                width: 97
                height: 36
                color: "#ffffff"
                text: car.tyresSurfaceTemperature[1] + "°C"
                anchors.left: parent.left
                anchors.leftMargin: 10
                font.pointSize: 30
                font.bold: true
            }

            QQC2.Label {
                id: txtTireRight1
                objectName: "txtTireRight1"
                x: 145
                y: 57
                width: 97
                height: 36
                color: "#ffffff"
                text: car.tyresSurfaceTemperature[2] + "°C"
                horizontalAlignment: Text.AlignRight
                anchors.rightMargin: 10
                anchors.right: parent.right
                font.pointSize: 30
                font.bold: true
            }

            QQC2.Label {
                id: txtTireRight2
                objectName: "txtTireRight2"
                x: 143
                y: 99
                width: 97
                height: 36
                color: "#ffffff"
                text: car.tyresSurfaceTemperature[3] + "°C"
                anchors.right: parent.right
                anchors.rightMargin: 10
                horizontalAlignment: Text.AlignRight
                font.pointSize: 30
                font.bold: true
            }
            border.color: "#808080"
        }

        QQC1.ProgressBar {
            id: txtEnergyERS
            objectName: "txtEnergyERS"
            width: 600
            height: 30
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 100
            value: carStatus.ersStoreEnergyPercentage
            minimumValue: 0
            maximumValue: 100

            style: ProgressBarStyle {
                background: Rectangle {
                    color: "black"
                    border.color: "yellow"
                    border.width: 1
                }
                progress: Rectangle {
                    color: "yellow"
                    border.color: "yellow"
                }
            }

            QQC2.Label {
                id: txtLevelERS
                objectName: "txtLevelERS"
                x: -29
                y: 0
                width: 19
                height: 34
                color: "#ffff00"
                text: carStatus.ersDeployMode
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.left
                anchors.rightMargin: 10
                verticalAlignment: Text.AlignVCenter
                font.capitalization: Font.AllUppercase
                horizontalAlignment: Text.AlignRight
                font.family: "Arial"
                font.pointSize: 28
                font.weight: Font.DemiBold
                font.bold: true

                Image {
                    id: image
                    x: 0
                    y: 0
                    width: 28
                    height: 28
                    sourceSize.height: 30
                    sourceSize.width: 30
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.left
                    anchors.rightMargin: 0
                    fillMode: Image.PreserveAspectFit
                    source: "images/lightning-outline-filled.png"
                }
            }
            QQC2.Label {
                id: txtPercentageERS
                objectName: "txtPercentageERS"
                y: 0
                width: 66
                height: 34
                color: "yellow"
                text: carStatus.ersStoreEnergyPercentage + "%"
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.right
                anchors.leftMargin: 10
                verticalAlignment: Text.AlignVCenter
                font.capitalization: Font.AllUppercase
                horizontalAlignment: Text.AlignLeft
                font.family: "Arial"
                anchors.rightMargin: 10
                font.pointSize: 28
                font.weight: Font.DemiBold
                font.bold: true
            }
        }

        //D Progress
        QQC1.ProgressBar {
            id: txtProgressD
            objectName: "txtProgressD"
            width: 250
            height: 30
            anchors.left: parent.left
            anchors.leftMargin: 100
            style: ProgressBarStyle {
                background: Rectangle {
                    color: "black"
                    border.color: "white"
                    border.width: 1
                }
                progress: Rectangle {
                    color: "white"
                    border.color: "white"
                }
            }
            QQC2.Label {
                id: txtD
                x: -29
                y: 0
                width: 19
                height: 34
                color: "#ffffff"
                text: qsTr("D")
                renderType: Text.NativeRendering
                verticalAlignment: Text.AlignVCenter
                font.capitalization: Font.AllUppercase
                horizontalAlignment: Text.AlignRight
                font.family: "Arial"
                anchors.rightMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.left
                font.pointSize: 28
                font.weight: Font.DemiBold
                font.bold: true
            }
            value: carStatus.ersDeployedThisLap
            minimumValue: 0
            maximumValue: 100
            anchors.bottomMargin: 40
            anchors.bottom: parent.bottom
        }

        QQC1.ProgressBar {
            id: progressH
            objectName: "txtProgressH"
            width: 250
            height: 30
            anchors.right: parent.right
            anchors.rightMargin: 100
            style: ProgressBarStyle {
                background: Rectangle {
                    color: "black"
                    border.color: "white"
                    border.width: 1
                }
                progress: Rectangle {
                    color: "white"
                    border.color: "white"
                }
            }
            QQC2.Label {
                id: txtH
                y: 0
                width: 19
                height: 34
                color: "#ffffff"
                text: qsTr("H")
                anchors.left: parent.right
                anchors.leftMargin: 10
                verticalAlignment: Text.AlignVCenter
                font.capitalization: Font.AllUppercase
                horizontalAlignment: Text.AlignRight
                font.family: "Arial"
                anchors.verticalCenter: parent.verticalCenter
                font.pointSize: 28
                font.weight: Font.DemiBold
                font.bold: true
                renderType: Text.NativeRendering
            }
            value: carStatus.ersHarvestedThisLap
            minimumValue: 0
            maximumValue: 100
            anchors.bottomMargin: 40
            anchors.bottom: parent.bottom
        }

        RowLayout {
            id: rectangle
            x: 20
            y: 20
            width: 735
            height: 44
            anchors.horizontalCenter: parent.horizontalCenter
            Image {
                id: led14
                x: 707
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_green.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led13
                x: 442
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_green.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led12
                x: 408
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_empty.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led11
                x: 374
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_empty.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led10
                x: 340
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_empty.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led9
                x: 306
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_red.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led8
                x: 272
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_red.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led7
                x: 238
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_red.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led6
                x: 204
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_red.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led5
                x: 170
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_red.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led4
                x: 136
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_blue.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led3
                x: 102
                y: -4
                anchors.verticalCenter: parent.verticalCenter
                width: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_blue.png"
                sourceSize.height: 30
                sourceSize.width: 30
            }

            Image {
                id: led2
                x: 68
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_blue.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led1
                x: 34
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_blue.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }

            Image {
                id: led0
                x: 0
                y: -4
                width: 28
                height: 28
                fillMode: Image.PreserveAspectFit
                source: "images/led_blue.png"
                sourceSize.height: 30
                sourceSize.width: 30
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }



}

/*##^##
Designer {
    D{i:0;3d-active-scene:-1}
}
##^##*/
