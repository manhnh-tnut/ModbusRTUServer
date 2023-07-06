$(function () {
    $("#toolbar").dxToolbar({
        items: [{
            widget: "dxButton",
            openedStateMode: 'shrink',
            location: "before",
            options: {
                icon: "menu",
                onClick: function () {
                    drawer.toggle();
                }
            }
        }, {
            "text": "Inverter Monitoring",
            "location": "before"
            // }, {
            //     "text": "Missed"
            // }, {
            //     "text": "Favorites",
            //     "location": "after"
        }]
    });

    const drawer = $("#drawer").dxDrawer({
        minSize: 45,
        revealMode: "expand",
        openedStateMode: "shrink",
        template: function () {
            return $("<div/>").dxMenu({
                width: 200,
                displayExpr: "text",
                orientation: "vertical",
                submenuDirection: "auto",
                hideSubmenuOnMouseLeave: true,
                animation: {
                    show: { type: 'fade', from: 0, to: 1, duration: 1000 },
                    hide: { type: 'fade', from: 1, to: 0, duration: 100 }
                },
                items: [
                    {
                        id: 1, text: "Home", icon: "home",
                        items: [
                            { id: 1_1, text: "Home", icon: "home", url: "/home" },
                            { id: 1_2, text: "About", icon: "check", url: "/about" },
                            { id: 1_3, text: "Trash", icon: "trash", url: "trash" },
                            { id: 1_4, text: "Spam", icon: "mention", url: "spam" }
                        ]
                    },
                    { id: 2, text: "About", icon: "check", url: "/about" },
                    { id: 3, text: "Trash", icon: "trash", url: "trash" },
                    { id: 4, text: "Spam", icon: "mention", url: "spam" }
                ],
                onItemClick: function (e) {
                    if (e.itemData.url) {
                        window.location.href = e.itemData.url;
                    } else {
                        drawer.show();
                    }
                }
            });
        }
    }).dxDrawer("instance");
});