"""
VoxelGPT plugin.

| Copyright 2017-2023, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import json
import os
import sys
import traceback

from bson import json_util

import fiftyone as fo
from fiftyone.core.utils import add_sys_path
import fiftyone.operators as foo
import fiftyone.operators.types as types


class AskVoxelGPT(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="ask_voxelgpt",
            label="Ask VoxelGPT",
            light_icon="/assets/icon-light.svg",
            dark_icon="/assets/icon-dark.svg",
            execute_as_generator=True,
            # dynamic=True,
        )

    def resolve_input(self, ctx):
        inputs = types.Object()
        inputs.str(
            "query",
            label="query",
            required=True,
            description="What would you like to view?",
        )
        return types.Property(inputs)

    def execute(self, ctx):
        query = ctx.params["query"]
        sample_collection = ctx.view if ctx.view is not None else ctx.dataset
        messages = []

        inject_voxelgpt_secrets(ctx)

        try:
            with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
                # pylint: disable=no-name-in-module
                from voxelgpt import ask_voxelgpt_generator

                streaming_message = None

                for response in ask_voxelgpt_generator(
                    query,
                    sample_collection=sample_collection,
                    dialect="string",
                    allow_streaming=True,
                ):
                    type = response["type"]
                    data = response["data"]

                    if type == "view":
                        yield self.view(ctx, data["view"])
                    elif type == "message":
                        kwargs = {}

                        if data["overwrite"]:
                            kwargs["overwrite_last"] = True

                        yield self.message(
                            ctx, data["message"], messages, **kwargs
                        )
                    elif type == "streaming":
                        kwargs = {}

                        if streaming_message is None:
                            streaming_message = data["content"]
                        else:
                            streaming_message += data["content"]
                            kwargs["overwrite_last"] = True

                        yield self.message(
                            ctx, streaming_message, messages, **kwargs
                        )

                        if data["last"]:
                            streaming_message = None
        except Exception as e:
            yield self.error(ctx, e)

    def view(self, ctx, view):
        if view != ctx.view:
            return ctx.trigger(
                "set_view",
                params=dict(view=serialize_view(view)),
            )

    def message(self, ctx, message, messages, overwrite_last=False):
        if overwrite_last:
            messages[-1] = message
        else:
            messages.append(message)

        outputs = types.Object()
        outputs.str("query", label="You")
        results = dict(query=ctx.params["query"])
        for i, msg in enumerate(messages, 1):
            field = "message" + str(i)
            outputs.str(field, label="VoxelGPT")
            results[field] = msg

        return ctx.trigger(
            "show_output",
            params=dict(
                outputs=types.Property(outputs).to_json(),
                results=results,
            ),
        )

    def error(self, ctx, exception):
        message = str(exception)
        trace = traceback.format_exc()
        view = types.Error(label=message, description=trace)
        outputs = types.Object()
        outputs.view("message", view)
        return ctx.trigger(
            "show_output",
            params=dict(outputs=types.Property(outputs).to_json()),
        )


class CountSamples(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="count_samples",
            label="Count samples",
            dynamic=True,
        )

    def resolve_input(self, ctx):
        inputs = types.Object()

        if ctx.view != ctx.dataset.view():
            choices = types.RadioGroup()
            choices.add_choice(
                "DATASET",
                label="Dataset",
                description="Count the number of samples in the dataset",
            )

            choices.add_choice(
                "VIEW",
                label="Current view",
                description="Count the number of samples in the current view",
            )

            inputs.enum(
                "target",
                choices.values(),
                required=True,
                default="VIEW",
                view=choices,
            )

        return types.Property(inputs, view=types.View(label="Count samples"))

    def execute(self, ctx):
        target = ctx.params.get("target", "DATASET")
        sample_collection = ctx.view if target == "VIEW" else ctx.dataset
        return {"count": 50}

    def resolve_output(self, ctx):
        target = ctx.params.get("target", "DATASET")
        outputs = types.Object()
        outputs.int(
            "count",
            label=f"Number of samples in the current {target.lower()}",
        )
        return types.Property(outputs)
    
class AskVoxelGPTPanel(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="ask_voxelgpt_panel",
            label="Ask VoxelGPT Panel",
            # execute_as_generator=True,
            dynamic=True,
        )

    def execute(self, ctx):
        return ['khai','khai2','khai3']
        # query = ctx.params["query"]
        # history = ctx.params.get("history", [])
        # chat_history, sample_collection, orig_view = self._parse_history(
        #     ctx, history
        # )

        # inject_voxelgpt_secrets(ctx)

        # try:
        #     with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
        #         # pylint: disable=import-error,no-name-in-module
        #         import db
        #         from voxelgpt import ask_voxelgpt_generator

        #         # Log user query
        #         table = db.table(db.UserQueryTable)
        #         ctx.params["query_id"] = table.insert_query(query)

        #         streaming_message = None

        #         for response in ask_voxelgpt_generator(
        #             query,
        #             sample_collection=sample_collection,
        #             chat_history=chat_history,
        #             dialect="markdown",
        #             allow_streaming=True,
        #         ):
        #             type = response["type"]
        #             data = response["data"]

        #             if type == "view":
        #                 if orig_view is not None:
        #                     message = (
        #                         "I'm remembering your previous view. Any "
        #                         "follow-up questions in this session will be "
        #                         "posed with respect to it"
        #                     )
        #                     yield self.message(
        #                         ctx, message, orig_view=orig_view
        #                     )

        #                 yield self.view(ctx, data["view"])
        #             elif type == "message":
        #                 kwargs = {}

        #                 if data["overwrite"]:
        #                     kwargs["overwrite_last"] = True

        #                 kwargs["history"] = data["history"]
        #                 yield self.message(ctx, data["message"], **kwargs)
        #             elif type == "streaming":
        #                 kwargs = {}

        #                 if streaming_message is None:
        #                     streaming_message = data["content"]
        #                 else:
        #                     streaming_message += data["content"]
        #                     kwargs["overwrite_last"] = True

        #                 if data["last"]:
        #                     kwargs["history"] = streaming_message

        #                 yield self.message(ctx, streaming_message, **kwargs)

        #                 if data["last"]:
        #                     streaming_message = None
        #             elif type == "warning":
        #                 yield self.warning(ctx, data["message"])
        # except Exception as e:
        #     yield self.error(ctx, e)
        # finally:
        #     yield self.done(ctx)

    def resolve_input(self, ctx):
        inputs = types.Object()

        if ctx.view != ctx.dataset.view():
            choices = types.RadioGroup()
            choices.add_choice(
                "DATASET",
                label="Dataset",
                description="Count the number of samples in the dataset",
            )

            choices.add_choice(
                "VIEW",
                label="Current view",
                description="Count the number of samples in the current view",
            )

            inputs.enum(
                "target",
                choices.values(),
                required=True,
                default="VIEW",
                view=choices,
            )

        return types.Property(inputs, view=types.View(label="Count samples"))

    def execute(self, ctx):
        target = ctx.params.get("target", "DATASET")
        sample_collection = ctx.view if target == "VIEW" else ctx.dataset
        return {"count": sample_collection.count()}

    def resolve_output(self, ctx):
        target = ctx.params.get("target", "DATASET")
        outputs = types.Object()
        outputs.int(
            "count",
            label=f"Number of samples in the current {target.lower()}",
        )


class OpenVoxelGPTPanel(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="open_voxelgpt_panel",
            label="Open VoxelGPT Panel",
            unlisted=True,
        )

    def resolve_placement(self, ctx):
        return types.Placement(
            types.Places.SAMPLES_GRID_ACTIONS,
            types.Button(
                label="Open AtlasVoxel",
                icon="/assets/icon-dark.svg",
                prompt=False,
            ),
        )

    def execute(self, ctx):
        ctx.trigger(
            "open_panel",
            params=dict(name="voxelgpt", isActive=True, layout="horizontal"),
        )


class OpenVoxelGPTPanelOnStartup(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="open_voxelgpt_panel_on_startup",
            label="Open VoxelGPT Panel",
            on_startup=True,
            unlisted=True,
        )

    def execute(self, ctx):
        open_on_startup = get_plugin_setting(
            ctx.dataset, self.plugin_name, "open_on_startup", default=False
        )
        if open_on_startup:
            ctx.trigger(
                "open_panel",
                params=dict(
                    name="voxelgpt", isActive=True, layout="horizontal"
                ),
            )


class VoteForQuery(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="vote_for_query",
            label="Vote For Query",
            unlisted=True,
        )

    def resolve_input(self, ctx):
        inputs = types.Object()
        inputs.str(
            "query_id",
            label="query_id",
            required=True,
            description="User Query to Vote For",
        )
        inputs.enum(
            "vote",
            ["upvote", "downvote"],
            label="Vote",
            required=True,
        )
        return types.Property(inputs)

    def execute(self, ctx):
        query_id = ctx.params["query_id"]
        vote = ctx.params["vote"]

        with add_sys_path(os.path.dirname(os.path.abspath(__file__))):
            # pylint: disable=import-error,no-name-in-module
            import db

            table = db.table(db.UserQueryTable)
            if vote == "upvote":
                table.upvote_query(query_id)
            elif vote == "downvote":
                table.downvote_query(query_id)
            else:
                raise ValueError(f"Invalid vote '{vote}'")


def get_plugin_setting(dataset, plugin_name, key, default=None):
    value = dataset.app_config.plugins.get(plugin_name, {}).get(key, None)

    if value is None:
        value = fo.app_config.plugins.get(plugin_name, {}).get(key, None)

    if value is None:
        value = default

    return value


def serialize_view(view):
    return json.loads(json_util.dumps(view._serialize()))


def deserialize_view(dataset, stages):
    return fo.DatasetView._build(dataset, json_util.loads(json.dumps(stages)))


def inject_voxelgpt_secrets(ctx):
    try:
        api_key = ctx.secrets["OPENAI_API_KEY"]
    except:
        api_key = None

    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key


def register(p):
    p.register(AskVoxelGPT)
    p.register(AskVoxelGPTPanel)
    p.register(OpenVoxelGPTPanel)
    p.register(OpenVoxelGPTPanelOnStartup)
    p.register(VoteForQuery)
    p.register(CountSamples)
