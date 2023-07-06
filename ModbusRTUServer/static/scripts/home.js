let socket = io();
let gridStore = new DevExpress.data.ArrayStore({
    key: "id",
    data: []
});
let chartStore = new DevExpress.data.ArrayStore({
    key: "time",
    data: []
});

$(function () {
    socket.on('connect', function () {
        console.log('connect')
    });

    socket.on('init', data => {
        gridStore = new DevExpress.data.ArrayStore({
            key: "id",
            data: data
        });
        chartStore = new DevExpress.data.ArrayStore({
            key: "time",
            data: data
        });

        $("#charContainer").dxChart({
            dataSource: {
                store: chartStore,
                reshapeOnPush: true
            },
            commonSeriesSettings: {
                argumentField: "time",
                valueField: "value",
                type: "spline",
                stepline: {
                    point: {
                        visible: false
                    }
                }
            },
            seriesTemplate: {
                nameField: "name"
            },
            label: {
                overlappingBehavior: 'hide'
            },
            // panes: [{
            //     name: "BYTE"
            // }, {
            //     name: "RESGISTER"
            // }],
            title: {
                text: "PHẦN MỀM GIÁM SÁT BIẾN TẦN",
                subtitle: {
                    text: "(Real-time)"
                }
            },
            loadingIndicator: {
                enabled: false
            },
            tooltip: {
                enabled: true,
                shared: true,
                argumentFormat: "shortDateShortTime",
                contentTemplate: function (pointInfo, element) {
                    var print = function (label, value) {
                        var span = $("<span>", {
                            "class": "tooltip-label",
                            text: label
                        });
                        element.append($("<div>", {
                            text: value
                        }).prepend(span));
                    };
                    print("", pointInfo.argumentText);
                    print("", pointInfo.valueText);
                }
            },
            crosshair: {
                enabled: true,
                horizontalLine: { visible: false }
            },
            argumentAxis: {
                argumentType: "datetime",
                minVisualRangeLength: { minutes: 10 },
                visualRange: {
                    length: "hour"
                }
            },
        });

        $("#gridContainer").dxDataGrid({
            dataSource: {
                store: gridStore,
                reshapeOnPush: true
            },
            repaintChangesOnly: true,
            highlightChanges: true,
            columnAutoWidth: true,
            showBorders: true,
            paging: {
                pageSize: 10
            },
            editing: {
                mode: "row",
                useIcons: true,
                allowAdding: true,
                allowUpdating: false,
                allowDeleting: true,
                refreshMode: "reshape",
            },
            columns: [{
                caption: '#',
                allowEditing: false,
                cellTemplate: function (container, options) {
                    container.text(options.row.rowIndex + 1)
                },
            },
            {
                dataField: "name",
                caption: "Name",
                validationRules: [{ type: "required" }]
            },
            {
                dataField: "desc",
                caption: "Description",
            },
            {
                dataField: "type",
                caption: "Type",
                lookup: {
                    dataSource: ['coils', 'discrete inputs', 'holding registers', 'input registers'],
                },
                validationRules: [{ type: "required" }]
            },
            {
                dataField: "reg",
                caption: "Register",
                dataType: "number",
                validationRules: [{ type: "required" }]
            },
            {
                dataField: "min",
                caption: "Min",
                dataType: "number",
            },
            {
                dataField: "max",
                caption: "Max",
                dataType: "number",
            },
            {
                dataField: "value",
                caption: "Value",
                allowEditing: false,
                cellTemplate: function (container, options) {
                    container.addClass(((options.data.min !== undefined && options.data.value < options.data.min) || (options.data.max !== undefined && options.data.value > options.data.max)) ? "error" : "success");
                    container.html(options.text);
                }
            }],
            onEditingStart: function (e) {
                console.log("EditingStart");
            },
            onInitNewRow: function (e) {
                console.log("InitNewRow");
            },
            onRowInserting: function (e) {
                console.log("RowInserting");
            },
            onRowInserted: function (e) {
                console.log("RowInserted");
                socket.emit('add', e.data);
            },
            onRowUpdating: function (e) {
                console.log("RowUpdating");
                if (e.newData.reg) {
                    e.cancel = true
                    DevExpress.ui.notify('Cannot update register', 'error', 600);
                }
            },
            onRowUpdated: function (e) {
                console.log("RowUpdated");
                socket.emit('update', e.data);
            },
            onRowRemoving: function (e) {
                console.log("RowRemoving");
            },
            onRowRemoved: function (e) {
                console.log("RowRemoved");
                socket.emit('remove', e.data);
            }
        });
    });

    socket.on('add', data => {
        chartStore.push([{ type: "insert", data: data }]);
        gridStore.push([{ type: "insert", data: data }]);
    });

    socket.on('update', data => {
        chartStore.push([{ type: "insert", data: data }]);
        gridStore.push([{ type: "update", key: data.id, data: data }]);
    });

    socket.on('remove', data => {
        gridStore.push([{ type: "remove", key: data.id, data: data }]);
    });

    socket.on('notify', data => {
        chartStore.push([{ type: "insert", data: data }]);
        gridStore.push([{ type: "update", key: data.id, data: data }]);
    });

    socket.on('message', message => {
        DevExpress.ui.notify(message, 'error', 600);
    });
});